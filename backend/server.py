
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Default route
@app.route('/')
def home():
    return "Welcome to the Flask server!"

# Example GET route
@app.route('/api/hello', methods=['GET'])
def say_hello():
    name = request.args.get('name', 'World')  # Get 'name' parameter from query string
    return jsonify({'message': f'Hello, {name}!'})

# Example POST route
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json  # Parse JSON body
    if not data:
        return jsonify({'error': 'No JSON body provided'}), 400
    return jsonify({'received': data})

# Example route for processing data
@app.route('/api/process', methods=['POST'])
def process():
    data = request.json
    if not data or 'input' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    processed = data['input'].upper()  # Example processing: convert to uppercase
    return jsonify({'processed': processed})

# 404 Error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
