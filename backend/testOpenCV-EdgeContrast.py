import cv2

cap = cv2.VideoCapture('media/videoplayback.mp4')

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Couldn't open the video.")
    exit()

# Loop through each frame in the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
        # Get the dimensions of the frame
    height, width, _ = frame.shape
    
    # Calculate the starting point of the bottom fourth of the frame
    start_y = int(height * 3 / 4)  # 3/4 of the height
    
    # Crop the bottom fourth of the frame
    bottom_quarter_frame = frame[start_y:, :]  # All columns, from the 3/4 height to the bottom

    # Process the frame (next steps)
    gray_frame = cv2.cvtColor(bottom_quarter_frame, cv2.COLOR_BGR2GRAY)
   
    # Apply Gaussian Blur to reduce noise (optional)
    blurred = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    # Adjust Canny edge detection thresholds for less sensitivity
    edges = cv2.Canny(blurred, 50, 150)  # Experiment with the thresholds
    cv2.imshow('Frame', edges)

    # Press 'q' to quit the video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()