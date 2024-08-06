from flask import Flask, request, jsonify
import os
import time
import base64
from datetime import datetime
from threading import Thread

app = Flask(__name__)
UPLOAD_FOLDER = '/home/nanshe/data/upload/'  # Set your upload folder path here

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def cleanup_old_files():
    while True:
        now = time.time()
        cutoff = now - 3600  # 1 hour ago
        for device_folder in os.listdir(UPLOAD_FOLDER):
            device_path = os.path.join(UPLOAD_FOLDER, device_folder)
            if os.path.isdir(device_path):
                for filename in os.listdir(device_path):
                    file_path = os.path.join(device_path, filename)
                    if os.path.isfile(file_path):
                        file_mtime = os.path.getmtime(file_path)
                        if file_mtime < cutoff:
                            os.remove(file_path)
        time.sleep(600)  # Run cleanup every 10 minutes



@app.route('/upload', methods=['POST'])
def upload_file():
    device_id = request.form.get('device_id')
    image = request.files.get('image')
    if not device_id or not image:
        return jsonify({'error': 'Device ID and image are required'}), 400

    # Get the original filename extension
    _, ext = os.path.splitext(secure_filename(image.filename))

    device_folder = os.path.join(UPLOAD_FOLDER, device_id)
    if not os.path.exists(device_folder):
        os.makedirs(device_folder)

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}{ext}"
    file_path = os.path.join(device_folder, filename)
    image.save(file_path)

    return jsonify({'message': 'File uploaded successfully'}), 200

#def upload_file():
#    device_id = request.form.get('device_id')
#    image = request.files.get('image')
#    if not device_id or not image:
#        return jsonify({'error': 'Device ID and image are required'}), 400
#
#    device_folder = os.path.join(UPLOAD_FOLDER, device_id)
#    if not os.path.exists(device_folder):
#        os.makedirs(device_folder)
#
#    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#    filename = f"{timestamp}.png"
#    file_path = os.path.join(device_folder, filename)
#    image.save(file_path)
#
#    return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    cleanup_thread = Thread(target=cleanup_old_files)
    cleanup_thread.daemon = True
    cleanup_thread.start()
    app.run(host='0.0.0.0', port=11435)

