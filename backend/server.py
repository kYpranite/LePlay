
from flask import Flask, render_template, request, jsonify, flash

import flask_uploads
import os
from flask_uploads import UploadSet


app = Flask(__name__)

# Default route
@app.route('/')
def home():
    return "Welcome to the Flask server!"
    

VIDEOS = tuple("mp4", "mov")
print (VIDEOS)
videos = UploadSet("videos", VIDEOS)
app.config["UPLOADED_PHOTOS_DEST"] = "./media"
app.config["SECRET_KEY"] = os.urandom(24)
flask_uploads.configure_uploads(app, videos)


@app.route("/api/upload", methods=['GET', 'POST'])
def upload():
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
