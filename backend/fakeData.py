from flask import Flask, send_from_directory
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Directory containing your video files
VIDEO_DIRECTORY = "/Users/tonynguyen/Desktop/media"
os.makedirs(VIDEO_DIRECTORY, exist_ok=True)

@app.route("/videos/<path:filename>", methods=["GET"])
def serve_video(filename):
    """Serve video files from the media directory."""
    return send_from_directory(VIDEO_DIRECTORY, filename)

if __name__ == "__main__":
    app.run(debug=True)