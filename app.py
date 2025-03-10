from flask import Flask, request, jsonify, render_template
import os
from inference_sdk import InferenceHTTPClient

app = Flask(__name__)

# Configure Roboflow client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="2Erh2NhihmT8RGeBGhpC"
)

# Set up upload folder
UPLOAD_FOLDER = 'static/uploads'
RESULTS_FOLDER = 'static/results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

# Ensure upload and results folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Perform inference using Roboflow
    try:
        result = CLIENT.infer(file_path, model_id="pothole-detection-2-28w0d/1")
        print("Raw Roboflow Response:", result)  # Log the raw response for debugging
    except Exception as e:
        return jsonify({'error': f'Inference failed: {str(e)}'}), 500

    # Check if predictions are empty
    if not result.get('predictions'):
        return jsonify({'error': 'No potholes detected'}), 400

    # Return the result with bounding box coordinates
    return jsonify({
        'message': 'Detection successful',
        'result': result['predictions'],  # Return only the predictions array
        'image_url': f'/static/uploads/{file.filename}'
    })

if __name__ == '__main__':
    app.run(debug=True)