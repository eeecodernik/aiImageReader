import re
import os
import pytesseract
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS
from anthropic import Anthropic
from PIL import Image

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to avoid cross-origin issues

# Set the path from the environment variable
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD', '/usr/bin/tesseract')

# Replace with your actual Anthropic API key
api_key = os.getenv('ANTHROPIC_API_KEY')
anthropic = Anthropic(api_key=api_key)

# Function to extract text from the uploaded image
def extract_text(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to analyze the extracted text and extract date, time, and destination
def analyze_text(text):
    date_pattern1 = r'\b(\d{2}[/,-]\d{2}[/,-]\d{4})\b'
    date_pattern2 = r'\b(\d{2}[/,-]\d{2}[/,-]\d{2})\b'
    time_pattern = r'\b(\d{2}:\d{2}:\d{2})\b'
    destination_pattern = r"Destination:\s*(.*)"

    # Extract information using regular expressions
    date_match = re.search(date_pattern1, text)
    if date_match is None:
        date_match = re.search(date_pattern2, text)
    time_match = re.search(time_pattern, text)
    destination_match = re.search(destination_pattern, text)

    date = date_match.group(0) if date_match else None
    time = time_match.group(0) if time_match else None
    destination = destination_match.group(1) if destination_match else None

    return date, time, destination

# Function to call the Anthropic API for additional analysis (if needed)
def call_anthropic_api(text):
    response = anthropic.complete(
        prompt="Analyze the following text to extract date, time, and destination:\n" + text,
        model="claude-3-5-sonnet-20240620",
        max_tokens=50
    )
    return response["completion"]

# Endpoint to handle image uploads and process them in memory
@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Process the uploaded image directly from memory
        image = Image.open(BytesIO(file.read()))
        text = extract_text(image)
        date, time, destination = analyze_text(text)

        # Optionally, call the Anthropic API
        # anthropic_response = call_anthropic_api(text)

        return jsonify({
            'date': date,
            'time': time,
            'destination': destination,
            'text': text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'API is running'}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
