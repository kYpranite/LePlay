import google.generativeai as genai
import time


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
    video_file = upload(file_name)
    check_file(video_file)
    response = generate(prompt, video_file)
    print(response)


def player_timestamp(key: str, file_name: str, players) -> None:
    """
    Similar functionality to run() but specifically asks for timestamps of when a 
    certain player- user inputted- is mentioned or highlighted in the video
    """
    video_file = upload(file_name)
    check_file(video_file)
    players = players.join(", ")
    response = generate(f"Generate a list of 10 timestamps of when any of these following players are mentioned: {players}. Only timestamp moments in which there is a basketball highlight happening. A highlight would be a 3-pointer, dunk, layup, block, steal. Use only sports commentator mentions, do not base any timestamps on visual mentions ALONE. Do not include any clips where the scoreboard is NOT visible. The ten timestamps you choose for this player should be the most exciting ones based on style (for example a cool dunk). These timestamps should be formatted in [MM:SS]->{player}’s FIRST name {player}’s LAST name and ONLY in this format. For example: [03:45]->John Smith. Do not provide explanations, summaries, or notes. Only produce the formatted timestamps.",
                        video_file)
    print(response)

    return response


def categorize(key: str, file_name: str) -> None:
    """
    Similar functionality to run() but specifically asks gemini to categorize the type
    of play that is occuring on screen
    """
    video_file = upload(file_name)
    check_file(video_file)
    response = generate("What was the one most notable part of the video clip (with a [MM:SS] timestamp)? \
                        Categorize only by 3-pointer, dunk, layup, block, assist, steal.", 
                        video_file)
    print(response)

    return response
