import cv2
import pytesseract
import numpy as np

def read_video_frame(cap, skip_frames=5):
    """Read and skip frames from the video."""
    for _ in range(skip_frames - 1):
        cap.read()  # Skip frames
    ret, frame = cap.read()
    return ret, frame

def get_total_frames(video_path):
    """Get the total number of frames in the video."""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total_frames

def get_frame_at_index(video_path, index):
    """Get a specific frame by its index."""
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, index)
    ret, frame = cap.read()
    cap.release()
    return ret, frame

def get_bottom_fourth(frame):
    """Extract the bottom fourth (Region of Interest) from a frame."""
    height, _, _ = frame.shape
    roi = frame[int(3 * height / 4):, :]
    return roi

def compute_frame_difference(prev_frame, current_frame):
    """Compute the absolute difference between two frames."""
    return cv2.absdiff(prev_frame, current_frame)

def threshold_difference(diff_frame, threshold_value=25):
    """Apply thresholding to isolate changes in the difference frame."""
    gray_diff = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_diff, threshold_value, 255, cv2.THRESH_BINARY)
    return thresh

def blacken_non_static_regions(prev_roi, current_roi, thresh):
    """Blackens non-static regions in the current region of interest (ROI)."""
    static_mask = cv2.bitwise_not(thresh)
    static_frame = cv2.bitwise_and(current_roi, current_roi, mask=static_mask)
    return static_frame

def accumulate_static_frames(accumulated_frame, static_frame):
    """
    Accumulates static frames over time to identify consistently static regions.

    Args:
        accumulated_frame (ndarray): Previously accumulated static frame.
        static_frame (ndarray): Current static frame.

    Returns:
        ndarray: Updated accumulated frame.
    """
    # Ensure both frames are float32 for compatibility with cv2.addWeighted
    static_frame = static_frame.astype(np.float32)
    accumulated_frame = static_frame.astype(np.float32)

    if accumulated_frame is None:
        # Initialize accumulated_frame with the same shape and type as static_frame
        accumulated_frame = np.zeros_like(static_frame, dtype=np.float32)

    # Ensure shapes match
    if accumulated_frame.shape != static_frame.shape:
        static_frame = cv2.resize(static_frame, (accumulated_frame.shape[1], accumulated_frame.shape[0]))

    # Weighted accumulation
    alpha = 0.05  # Weight for the current frame
    #print("Static Frame Type:", static_frame.dtype, "Shape:", static_frame.shape)
    #print("Accumulated Frame Type:", accumulated_frame.dtype, "Shape:", accumulated_frame.shape)

    accumulated_frame = cv2.addWeighted(static_frame, alpha, accumulated_frame, 1 - alpha, 0)

    # Convert back to 8-bit for display
    return cv2.convertScaleAbs(accumulated_frame)

def get_edges(frame):
    """Extract edges from a frame using the Canny edge detector."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)
    return edges

def accumulate_edges(accumulated_edges, current_edges, weight, frame_index, max_frames):
    """Accumulate edge information over multiple frames with weighted averaging."""
    if accumulated_edges is None:
        # Initialize the accumulated edges as a float array for weighted accumulation
        accumulated_edges = np.zeros_like(current_edges, dtype=np.float64)

    # Ensure the same size and type (float64) for the current edges
    current_edges = current_edges.astype(np.float64)
    accumulated_edges = accumulated_edges.astype(np.float64)
    

    # Add the weighted current edges to the accumulated edges
    accumulated_edges += current_edges * weight

    # Optionally normalize the accumulated edges based on the number of frames processed
    if frame_index == max_frames - 1:  # If this is the last frame
        accumulated_edges /= max_frames

    # Cast the result back to uint16 for the final edge map
    accumulated_edges = np.clip(accumulated_edges, 0, 255)  # Ensure values are within valid range
    accumulated_edges = accumulated_edges.astype(np.uint16)  # Convert back to uint16 for storage

    return np.uint16(np.clip(accumulated_edges, 0, 255))


def find_consistent_edges(accumulated_edges, threshold):
    """Threshold the accumulated edge map to find consistent edges."""
    consistent_edges = (accumulated_edges >= threshold).astype(np.uint8) * 255
    return consistent_edges

def find_rectangle_from_edges(edges):
    """Find rectangles in the edge map using contours."""
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangles = []
    for contour in contours:
        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(contour, epsilon=0.02 * cv2.arcLength(contour, True), closed=True)
        if len(approx) == 4:  # Check if the polygon has 4 vertices
            rectangles.append(cv2.boundingRect(approx))  # Add the bounding rectangle
    return rectangles

def find_median_edge_location(edges):
    """Find the median location of an edge in the image."""
    # Get the coordinates of the edge pixels
    edge_points = np.column_stack(np.where(edges > 0))
    
    # Check if there are any edges found
    if edge_points.size == 0:
        return None  # No edges found
    
    # Calculate the median of the x and y coordinates
    median_y = np.median(edge_points[:, 0])  # Median of y coordinates
    median_x = np.median(edge_points[:, 1])  # Median of x coordinates
    
    return (int(median_x), int(median_y))

def get_frame_size(frame):
    """
    Get the size (width and height) of the frame.
    
    :param frame: The image frame (NumPy array).
    :return: A tuple (width, height).
    """
    height, width = frame.shape[:2]  # Get height and width from the shape of the frame
    return width, height


def main(video_path, num_frames=30):
    """Main function to process the video and find the most consistent rectangle."""
    total_frames = get_total_frames(video_path)
    frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)

    accumulated_edges = None

    for idx in frame_indices:
        print(f"Processing frame {idx}/{num_frames}")

        ret, frame = get_frame_at_index(video_path, idx)
        if not ret:
            print(f"Error reading frame at index {idx}")
            continue

        # Extract Region of Interest (ROI)
        roi = get_bottom_fourth(frame)

        # Get edges from the current ROI
        edges = get_edges(roi)

        # Get weight
        weight = 0.2 / num_frames

        # Accumulate edges
        accumulated_edges = accumulate_edges(accumulated_edges, edges, weight, frame_index=idx, max_frames=num_frames)

    # Normalize accumulated edges to fit in 8-bit range for visualization
    if accumulated_edges is not None:
        accumulated_edges = np.clip(accumulated_edges, 0, 255).astype(np.uint8)

    # Threshold the accumulated edges to find consistent edges
    consistent_edges = find_consistent_edges(accumulated_edges, threshold=num_frames // 2)

    median_location = find_median_edge_location(consistent_edges)

    if median_location:
        print(f"Median edge location: {median_location}")
        cv2.circle(frame, median_location, 10, (0, 0, 255), -1)  # Draw a circle at the median location
        cv2.imshow('Frame with Median Edge Location', frame)
    else:
        print("No edges found.")

    cv2.imshow("Consistent Edges", consistent_edges)

    # Define the area (ROI) you want to focus on, e.g., top-left and bottom-right corners
    roi_top_left = (int(median_location[0] - get_frame_size(consistent_edges)[0] // 3), int(median_location[1] - get_frame_size(consistent_edges)[1] // 4))

    roi_bottom_right = (int(median_location[0] + get_frame_size(consistent_edges)[0] // 3), int(median_location[1] + get_frame_size(consistent_edges)[1] // 4))

    
    # Ensure roi_top_left is not outside the image boundaries
    roi_top_left = (
        max(roi_top_left[0], 0),  # Prevent x from going below 0
        max(roi_top_left[1], 0)   # Prevent y from going below 0
    )
    
    # Ensure roi_bottom_right is not outside the image boundaries
    roi_bottom_right = (
        min(roi_bottom_right[0], get_frame_size(consistent_edges)[0]),  # Prevent x from exceeding frame width
        min(roi_bottom_right[1], get_frame_size(consistent_edges)[1])  # Prevent y from exceeding frame height
    )
    
    cap = cv2.VideoCapture('media/0.mp4')

    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error: Couldn't open the video.")
        exit()

    frame_counter = 0

    # Loop through each frame in the video
    while True:
        # Read every 5th frame
        ret, frame = read_video_frame(cap, skip_frames=15)
        if not ret:
            break  # Exit loop if no more frames

        frame_counter += 1

        if ret:
            bottom_fourth = get_bottom_fourth(frame)  # Pass only the frame here

            # Assuming 'frame' is the image you're working with
            # Draw the rectangle on the frame
            cv2.rectangle(bottom_fourth, roi_top_left, roi_bottom_right, (0, 255, 0), 2)  # (0, 255, 0) is the color green, and 2 is the thickness

            cv2.imshow("Raw roi", bottom_fourth)
        else:
            print(f"Error reading frame at index {frame_indices[10]}")

        # Press 'q' to quit the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Run the main function with the video path
main('media/0.mp4')
