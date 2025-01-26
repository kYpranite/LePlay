import cv2

cap = cv2.VideoCapture("./media/lebron.mp4") 

cap.set(cv2.CAP_PROP_POS_FRAMES, 1)

frame = cap.read()[1]

height, width = frame.shape[:2]
start_row = int(height * 3 / 4)
end_row = height
frame = frame[int(height*3/4):height, 0:width]

def scoreboard_detection(image, width, height):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    canny_points = cv2.Canny(gray, 200, 200)

    row_indexes = []

    for i in range(len(canny_points)):
        count = 0
        for j in range(len(canny_points[i])):
            if canny_points[i][j] == 255:
                count += 1
        if count > 80:
            row_indexes.append(i)


    bottom_row_index = max(row_indexes)
    upper_row_index = min(row_indexes)

    scaled = gray[upper_row_index:bottom_row_index, 0:width]
    return scaled
