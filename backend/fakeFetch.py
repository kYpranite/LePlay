
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json

app = Flask(__name__, static_folder='static')
CORS(app)

# Load JSON data
with open('fakedata.json') as f:
    data = json.load(f)

# Serve frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# API endpoint
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5050)