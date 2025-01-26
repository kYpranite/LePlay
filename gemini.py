import google.generativeai as genai
import time
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


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


def run(key: str, file_name: str, prompt: str) -> None:
    """
    Runs the program in its entirety:
    1. Configures the API key
    2. Uploads the video with the file API
    3. Checks that upload was successful
    4. Generates response based off given arguements for prompt and file_name
    5. Prints out the resposne to the query
    """
    configure(key)
    video_file = upload(file_name)
    check_file(video_file)
    response = generate(prompt, video_file)
    print(response)


def player_timestamp(key: str, file_name: str) -> None:
    """
    Similar functionality to run() but specifically asks for timestamps of when a 
    certain player- user inputted- is mentioned or highlighted in the video
    """
    configure(key)
    video_file = upload(file_name)
    check_file(video_file)
    player = input("What player do you want to see?: ")
    response = generate(f"Give me the timestamps of when {player} is mentioned", video_file)
    print(response)


def categorize(key: str, file_name: str) -> None:
    """
    Similar functionality to run() but specifically asks gemini to categorize the type
    of play that is occuring on screen
    """
    configure(key)
    video_file = upload(file_name)
    check_file(video_file)
    response = generate("What happened in the video clip? Categorize only by 3 pointer, dunk, layup, block, assist, steal, etc.", 
                        video_file)
    print(response)


def main() -> None:
    key = os.getenv("key")
    file_name =  input("Enter Video File: ")
    prompt = input("Enter Prompt: ")
    run(key, file_name, prompt)
    player_timestamp(key, file_name)
    categorize(key, file_name)


if __name__ == "__main__":
    main()