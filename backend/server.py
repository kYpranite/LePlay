
from flask import Flask, render_template, request, jsonify, flash
import subprocess
import math
import os
from flask_cors import CORS
from flask_uploads import UploadSet
import flask_uploads


app = Flask(__name__)

# Default route
@app.route('/')
def home():
    return "Welcome to the Flask server!"
    

VIDEOS = ["mp4"]
print (VIDEOS)
videos = UploadSet("videos", VIDEOS)
app.config["UPLOADED_VIDEOS_DEST"] = "media/unprocessed"
app.config["SECRET_KEY"] = os.urandom(24)
flask_uploads.configure_uploads(app, videos)
    
def split_video(path, chunk_duration):
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        duration = float(result.stdout.strip())
        num_chunks = math.ceil(duration / chunk_duration)
        for i in range(num_chunks):
            start_time = i * chunk_duration
            output_file = os.path.join("./media/clips", f"chunk_{i+1}.mp4")

            # FFmpeg command to extract a chunk
            command = [
                'ffmpeg', '-i', path, '-ss', str(start_time),
                '-t', str(chunk_duration), '-c', 'copy', output_file
            ]

            print(f"Creating chunk {i+1}/{num_chunks}: {output_file}")
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        
        
    
    

@app.route("/api/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'video' in request.files:
        fileName = videos.save(request.files['video'])
        split_video("./media/unprocessed/" + fileName ,20*60)
        return "Successful!!"
    return
    


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)