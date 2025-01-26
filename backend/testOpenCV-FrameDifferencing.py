import cv2
import numpy as np

def read_video_frame(cap, skip_frames=5):
    """Read and skip frames from the video."""
    for _ in range(skip_frames - 1):
        cap.read()  # Skip frames
    ret, frame = cap.read()
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
    """
    Blackens non-static regions in the current region of interest (ROI).

    Args:
        prev_roi (ndarray): The bottom fourth of the previous frame.
        current_roi (ndarray): The bottom fourth of the current frame.
        thresh (ndarray): Threshold mask isolating moving regions.

    Returns:
        ndarray: Frame with non-static regions blackened.
    """
    # Invert the threshold mask to focus on static regions
    static_mask = cv2.bitwise_not(thresh)

    # Apply the static mask to the current region of interest
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
    if accumulated_frame is None:
        return static_frame  # Initialize with the first static frame
    return cv2.bitwise_and(accumulated_frame, static_frame)

def find_static_regions(accumulated_frame, min_width=100, min_height=100):
    """Find static regions using contours."""
    gray = cv2.cvtColor(accumulated_frame, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    static_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > min_width and h > min_height:  # Filter small contours
            static_regions.append((x, y, w, h))
    return static_regions

def draw_bounding_rectangles(frame, regions):
    """Draw rectangles around detected regions on the frame."""
    for (x, y, w, h) in regions:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

def main(video_path):
    """Main function to process the video."""
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    prev_frame = None
    accumulated_frame = None
    frame_counter = 0

    while True:
        # Read every 5th frame
        ret, frame = read_video_frame(cap, skip_frames=1)
        if not ret:
            break  # Exit loop if no more frames

        frame_counter += 1

        # Extract Region of Interest (ROI)
        roi = get_bottom_fourth(frame)

        # Initialize prev_frame on the first iteration
        if prev_frame is None:
            prev_frame = roi            
            continue

        # Reset accumulated_frame 
        if frame_counter % 300 == 0:
            accumulated_frame = static_frame

        # Compute frame difference
        diff_frame = compute_frame_difference(prev_frame, roi)

        # Threshold the difference
        thresh_frame = threshold_difference(diff_frame)

        # Find static regions
        # static_regions = find_static_regions(thresh_frame)

        # Draw bounding rectangles on ROI
        # draw_bounding_rectangles(roi, static_regions)

        static_frame = blacken_non_static_regions(prev_frame, roi, thresh_frame)
         
        accumulated_frame = accumulate_static_frames(accumulated_frame, static_frame)

        # Detect and display rectangles every 30 frames
        if frame_counter % 30 == 0 and accumulated_frame is not None:
            static_regions = find_static_regions(accumulated_frame)
            draw_bounding_rectangles(accumulated_frame, static_regions)

        # Combine the original ROI and the static frame side-by-side
        combined_display = cv2.hconcat([roi, accumulated_frame])

        # Display the combined view
        cv2.imshow('Original ROI and Augmented ROI', combined_display)

        # Update prev_frame
        prev_frame = roi

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the main function with the video path
main('media/videoplayback.mp4')
