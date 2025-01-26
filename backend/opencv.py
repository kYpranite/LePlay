import os
import cv2
import pytesseract
from pathlib import Path
import google.generativeai as genai
import json
import re

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

def create_clips_data_list(dir_path):

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
    return output_list

def create_clip_json(dir_path):

    clips_data_list = create_clips_data_list(dir_path)

    with open('./chat_gpt_prompt.txt', 'r') as file:
        # Read the contents of the file
        gemini_input = file.read()

    print(gemini_input)
    gemini_input = str(gemini_input) + "\n\n" + str(clips_data_list)

    genai.configure(api_key="AIzaSyCgE7Gj8lu7-a2mTLfKUkzlln2OLhJ8E_k")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(gemini_input)
    print(response.text)
    print(type(response))
    print(type(response.text))
    
    return response.text

def score(quarter, team_a_score, team_b_score, time_remaining):
    SCORE_WEIGHT = 0.5
    QUARTER_WEIGHT = 0.3
    TIME_REMAINING_WEIGHT = 0.2
    
    MAX_GAP = 30
    
    difference = abs(team_a_score - team_b_score) 
    unscaled = 1-min(difference/MAX_GAP, 1)
    total = team_a_score + team_b_score
    scaling_factor = total/200
    
    score_factor = min(unscaled * scaling_factor,1)
    quarter_factor = quarter/4
    time_remaining_factor = 1 - time_remaining/720
    

        
    return SCORE_WEIGHT*score_factor + QUARTER_WEIGHT*quarter_factor + TIME_REMAINING_WEIGHT*time_remaining_factor
def convert_to_seconds(timestamp_str):
    """
    Converts a timestamp string in "MM:SS" format to total seconds.
    """
    if ":" in timestamp_str:
        minutes, seconds = map(int, timestamp_str.split(":"))
        return minutes * 60 + seconds
    else:
        return timestamp_str

def clip_score_json(dir_path):
    response = create_clip_json(dir_path)
    clip_json = response.replace("```json","").replace("```","")
    json_list = json.loads(clip_json)

    print(type(json_list))
    print(json_list)
    print("HERE")
    

    # Regular expression to match JSON objects or arrays
    # json_pattern = r"(\{.*?\}|\[.*?\])"

    # Find all matches in the text
    # json_matches = re.findall(json_pattern, clip_json, re.DOTALL)

    # List to store valid JSON objects
    # json_list = {
    #     "videos": []
    # }

    # print(type(json_list))

    # Process each JSON-like match
    # for json_str in json_matches:
    #     try:
    #         Parse the JSON string to validate it
    #         parsed_json = json.loads(json_str)
    #         json_list["videos"].append(parsed_json)
    #     except json.JSONDecodeError:
    #         print(f"Invalid JSON found and skipped: {json_str[:50]}...")
    # json_string = json.dumps(clip_json)
    #json_list = json.loads(json_string)

    print(type(json_list["videos"]))
    
    clip_score_json_object = {
        "items": [] 
    }

    for vid in json_list["videos"]:
        clip_score = score((int(vid["quarter"])),int(vid["score1"]),int(vid["score2"]),convert_to_seconds(vid["time"]))
        new_item = {"path": vid["file_path"], "score": clip_score}
        clip_score_json_object["items"].append(new_item)

    return clip_score_json_object

print("final")
print(clip_score_json('./media/clips'))
print("finished")

