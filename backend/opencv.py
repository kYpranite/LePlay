import cv2
import pytesseract
from pathlib import Path

# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def scoreboard_detection(image, width, height):
    try:
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
    except:
        raise



def extract_scoreboard_at_frame(cap, frame=1):
    try:    
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)

        initial = cap.read()[1]

        # get bottom fourth of frame
        height, width = initial.shape[:2]
        start_row = int(height * 3 / 4)
        end_row = height
        image = initial[int(height*3/4):height, 0:width]

        # converts to grayscale and crops frame further
        gray = scoreboard_detection(image, width, height)
        # enlarge
        gray = cv2.resize(gray, (0, 0), fx=8, fy=8)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # cv2.imwrite("extracted_frame.jpg", thresh)
        custom_config = r"-c tessedit_char_whitelist='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789: ' --psm 6"
        multiline_output = pytesseract.image_to_string(thresh, config=custom_config)  
        singleline_output = " ".join(multiline_output.splitlines())

        return singleline_output
        # cv2.imshow("Extracted Frame", thresh)
        # cv2.waitKey(0)
        # # Release resources
        # cap.release()
        # cv2.destroyAllWindows()
    except:
        return -1

def create_clip_json(dir_path):

    vid_list = []
    dir_path = Path(dir_path)

    print("created dir_path")
    for f in dir_path.iterdir():
        if f.is_file() and f.suffix == '.mp4':
            vid_list.append(f)

    print("created vid_list")

    output_list = []
    for vid in vid_list:
        print("Working on a vid...")
        cap = cv2.VideoCapture(vid)
        frame_interval = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))/10
        extracted_string_list = []
        for i in range(0,10):
            extracted_string = extract_scoreboard_at_frame(cap,0+(frame_interval * i))
            if extracted_string != -1:
                extracted_string_list.append(extracted_string)
        output_list.append([vid,extracted_string_list])

    print("finished, about to create json")
    print(output_list)
    #json_output = jsonify(output_list)
    #print(json_output)
    return

create_clip_json('media/')

