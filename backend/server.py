
from flask import Flask, render_template, request, jsonify, flash

import flask_uploads
import os
from flask_cors import CORS
from flask_uploads import UploadSet


app = Flask(__name__)

# Default route
@app.route('/')
def home():
    return "Welcome to the Flask server!"
    

VIDEOS = ["mp4"]
print (VIDEOS)
videos = UploadSet("videos", VIDEOS)
app.config["UPLOADED_VIDEOS_DEST"] = "media/"
app.config["SECRET_KEY"] = os.urandom(24)
flask_uploads.configure_uploads(app, videos)


@app.route("/api/upload", methods=['GET', 'POST'])
def upload():
    print("works")
    if request.method == 'POST' and 'video' in request.files:
        videos.save(request.files['video'])
        flash("Photo saved successfully.")
        return render_template('upload.html')
    return render_template('upload.html')
    


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
