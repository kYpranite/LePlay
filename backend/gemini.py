import google.generativeai as genai
import time
import os

def configure(key: str) -> None:
    """
    Configures the API using given API key
    """
    genai.configure(api_key=key)


def upload(file_name: str) -> str:
    """
    Given a file name, upload to the Genarative AI and return the upload.
    """
    video_file = genai.upload_file(path=file_name)
    return video_file


def check_file(video_file:str) -> None | ValueError:
    """
    Given an uploaded video file, verify that the file is ready to use
    """
    while video_file.state.name == "PROCESSING":
        time.sleep(10)
        video_file = genai.get_file(video_file.name)
    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)


def generate(prompt: str, video_file: str) -> str:
    """
    Given a video file and user inputted prompt, generate and return a response
    """
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([video_file, prompt],
                                  request_options={"timeout": 600})
    return response.candidates[0].content.parts[0].text


def player_timestamp(file_name: str, players: list, instruction) -> str:
    """
    Similar functionality to run() but specifically asks for timestamps of when a 
    certain player- user inputted- is mentioned or highlighted in the video
    """
    print ("Uploading file " + file_name)
    video_file = upload(file_name)
    check_file(video_file)
    players = ", ".join(players)
    print ("Prompting Gemini")
    response = generate(f"Generate a list of 10 timestamps of when any of these following players are mentioned: {players}. Only timestamp moments in which there is a basketball highlight happening. A highlight would be a 3-pointer, dunk, layup, block, steal. Place extra emphasis on these events or instructions if there are any after the colon: {instruction}. Use only sports commentator mentions, do not base any timestamps on visual mentions ALONE. Do not include any clips where the scoreboard is NOT visible. Do NOT add timestamps for other players than the ones we mentioned. The ten timestamps you choose for these players should be the most exciting ones based on style (for example a cool dunk) and with a slight preference for scoring highlights. These timestamps should be formatted in [MM:SS]->FIRST name LAST name and ONLY in this format and ONLY for the specified players. For example: [03:45]->John Smith. Do not provide explanations, summaries, any other text, or notes. Only produce the formatted timestamps.", video_file)
    print(response)

    return response


def categorize(video_file: str) -> str:
    """
    Similar functionality to run() but specifically asks gemini to categorize the type
    of play that is occuring on screen
    """
    response = generate("What was the one most notable part of the video clip (with a [MM:SS] timestamp)? \
                        Categorize only by 3-pointer, dunk, layup, block, assist, steal.", 
                        video_file)
    print(response)

    return response

def upload_all(directory: str):
    """
    Upload all files in the specified directory using upload()
    """
    video_list = []
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            result = upload(file_path)
            print(f"Uploaded {file_name}: {result}")
            video_list.append(result)
    return video_list

def categorize_all(video_list: list):
    for video_file in video_list:
        categorize(video_file)
