import importlib
import subprocess
import sys
import hashlib
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime

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

# Define your upload folder here
UPLOAD_FOLDER = '\~/data/upload/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Limit the types of files that can be uploaded (for security reasons)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
upload_status = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

@app.route('/upload', methods=['POST'])
def upload_file():
    device_id = request.form.get('device_id')
    image = request.files.get('image')
    client_md5 = request.form.get('md5')

    if not device_id or not image or not client_md5:
        return jsonify({'error': 'Device ID, image, and MD5 are required'}), 400

    if not allowed_file(image.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    device_folder = os.path.join(UPLOAD_FOLDER, device_id)
    if not os.path.exists(device_folder):
        os.makedirs(device_folder)

    # Set the upload start flag
    upload_status[device_id] = 'uploading'

    # Get the original filename extension
    _, ext = os.path.splitext(secure_filename(image.filename))

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}{ext}"
    file_path = os.path.join(device_folder, filename)
    image.save(file_path)

    # Calculate the MD5 checksum of the uploaded file
    server_md5 = calculate_md5(file_path)

    if client_md5 != server_md5:
        upload_status[device_id] = 'failed'
        os.remove(file_path)
        return jsonify({'error': 'MD5 checksum does not match'}), 400

    # Update the flag to indicate the upload is complete and successful
    upload_status[device_id] = 'completed'
    # Here you could add a notification to other applications

    return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11435)

