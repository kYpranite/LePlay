import cv2
import pytesseract
import numpy

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

cap = cv2.VideoCapture("./media/jeremy.mp4") 

cap.set(cv2.CAP_PROP_POS_FRAMES, 1)

initial = cap.read()[1]

height, width = initial.shape[:2]
start_row = int(height * 3 / 4)
end_row = height
image = initial[int(height*3/4):height, 0:width]

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

gray = scoreboard_detection(image, width, height)
gray = cv2.resize(gray, (0, 0), fx=8, fy=8)
blur = cv2.GaussianBlur(gray, (3, 3), 0)

thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cv2.imwrite("extracted_frame.jpg", thresh)

output = pytesseract.image_to_string(thresh, config='--psm 6')
print (output)
cv2.imshow("Extracted Frame", thresh)
cv2.waitKey(0)
# Release resources
cap.release()
cv2.destroyAllWindows()

