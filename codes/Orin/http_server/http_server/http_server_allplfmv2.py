import importlib
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import flask
except ImportError:
    print("Flask is not installed. Installing...")
    install('Flask')
    print("Flask has been installed. Reloading script.")
    # Reload the script after installing Flask
    python = sys.executable
    sys.exit(subprocess.call([python] + sys.argv))



from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Define your upload folder here
UPLOAD_FOLDER = '~/data/upload/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Limit the types of files that can be uploaded (for security reasons)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    device_id = request.form.get('device_id')
    image = request.files.get('image')

    if not device_id or not image:
        return jsonify({'error': 'Device ID and image are required'}), 400

    if not allowed_file(image.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    device_folder = os.path.join(UPLOAD_FOLDER, device_id)
    if not os.path.exists(device_folder):
        os.makedirs(device_folder)

    # Get the original filename extension
    _, ext = os.path.splitext(secure_filename(image.filename))

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}{ext}"
    file_path = os.path.join(device_folder, filename)
    image.save(file_path)

    return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11435)
