from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configurations
app.config["UPLOADED_VIDEOS_DEST"] = "media/"
app.config["SECRET_KEY"] = os.urandom(24)

# Ensure the media directory exists
os.makedirs(app.config["UPLOADED_VIDEOS_DEST"], exist_ok=True)

@app.route("/api/upload", methods=["POST"])
def upload():
    try:
        # Access the form data
        video = request.files.get("video")
        players = request.form.getlist("players")  # Extracting array of strings
        instructions = request.form.get("instruction")
        print(video, players, instructions)

        # Validate incoming data
        if not video or not players:
            return jsonify({"error": "Missing required fields"}), 400

        # Save the video file
        video_filename = os.path.join(app.config["UPLOADED_VIDEOS_DEST"], video.filename)
        video.save(video_filename)

        # Response
        return jsonify({
            "message": "Data uploaded successfully",
            "video": video.filename,
            "players": players,
            "instructions": instructions
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
