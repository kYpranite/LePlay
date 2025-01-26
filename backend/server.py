
from flask import Flask, render_template, request, jsonify, flash, send_from_directory
import subprocess
import math
import os
from flask_cors import CORS
from flask_uploads import UploadSet
import re
import flask_uploads

import random
from gemini import *
from timestamps import *
from Clip import Clip

app = Flask(__name__)
GEMINI_API_KEY = "AIzaSyDVmfRNFHR4aSvpsLg79qmBOcdENIvUpe8"
configure(GEMINI_API_KEY)

# Default route
@app.route('/')
def home():
    return "Welcome to the Flask server!"
    

VIDEOS = ["mp4"]
videos = UploadSet("videos", VIDEOS)
app.config["UPLOADED_VIDEOS_DEST"] = "media/unprocessed"
app.config["VIDEO_FOLDER"] = "media/clips"
app.config["SECRET_KEY"] = os.urandom(24)
chunk_duration = 20*60
flask_uploads.configure_uploads(app, videos)

def convert_to_seconds(timestamp_str):
    """
    Converts a timestamp string in "MM:SS" format to total seconds.
    """
    minutes, seconds = map(int, timestamp_str.split(":"))
    return minutes * 60 + seconds

    
def split_video(path, chunk_duration, file_name):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    chunk_names = []
    duration = float(result.stdout.strip())
    num_chunks = math.ceil(duration / chunk_duration)
    for i in range(num_chunks):
        start_time = i * chunk_duration
        no_extension = re.match(r"(.+)\..+", file_name).group(1)
        output_file = os.path.join("./media/chunks/" + f"{no_extension}_chunk_{i+1}.mp4")
        chunk_names.append(output_file)
        # FFmpeg command to extract a chunk
        command = [
            'ffmpeg', '-i', path, '-ss', str(start_time),
            '-t', str(chunk_duration), '-c', 'copy', output_file
        ]

        print(f"Creating chunk {i+1}/{num_chunks}: {output_file}")
        print (path)
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return chunk_names
    
def get_timestamps(chunk_path, players):
    print("Generating timestamps")
    timestamps = player_timestamp(chunk_path, players)
    return create_name_timestamp(timestamps)
    
def process_timestamps(timestamps, file_name):
    match = re.search(r'_chunk_(\d+)\.mp4', file_name)
    chunk_number = int(match.group(1))
    
    processed = []
    for item in timestamps:
        seconds = convert_to_seconds(item["timestamp"]) + (chunk_number - 1) * chunk_duration
        start_time = max(seconds - 7, 0)
        end_time = seconds + 8
        # self, path, start_time, end_time, chunk, category, player_first, player_last
        processed.append(Clip(start_time, end_time, chunk_number, item["first_name"], item["last_name"]))
    return processed
        
def createClips(timestamps, original_path):
    print ("Creating clips")
    print(timestamps)
    for i, clip in enumerate(timestamps):
        start_time = clip.start_time
        duration = clip.end_time - clip.start_time
        output_file = f"./media/clips/clip{i+1}_{clip.chunk}_{clip.player_first}_{clip.player_last}.mp4"
        print (output_file)
        # Construct the ffmpeg command
        ffmpeg_command = [
            "ffmpeg",
            "-i", original_path,  # Input main video
            "-ss", str(start_time),  # Start time
            "-t", str(duration),  # Clip duration
            "-c:v", "libx264",  # Video codec
            "-c:a", "aac",  # Audio codec
            "-strict", "experimental",  # Ensure compatibility
            output_file  # Output file
        ]
        
        # Run the command
        print(f"Creating clip: {output_file}")
        subprocess.run(ffmpeg_command, check=True)
        print(timestamps)

def processVideo(file_name, players):
    chunks = split_video("./media/unprocessed/" + file_name, chunk_duration, file_name)
    for file in chunks:
        timestamps = get_timestamps(file, players)
        processed = process_timestamps(timestamps, file)
        createClips(processed, "./media/unprocessed/" + file_name)
    return "Success"        

@app.route("/api/upload", methods=['GET', 'POST'])
def upload():
    print(request)
    if request.method == 'POST' and 'video' in request.files:
        file_name = videos.save(request.files['video'])
        processVideo(file_name, ["LeBron James", "Stephen Curry"])
        return "Successful!!"
    return "Sad face"
    
@app.route("/api/clips/<clip>")
def get_clip(clip):
    return send_from_directory(app.config["VIDEO_FOLDER"], clip)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)