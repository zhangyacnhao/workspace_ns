import requests
import hashlib

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

file_path = 'test.jpeg'
#file_path = 'testfile.png'
device_id = '8888'

md5_checksum = calculate_md5(file_path)

#upload_url = 'http://localhost:11435/upload'
upload_url = 'http://192.168.29.238:11435/upload'

files = {'image': open(file_path, 'rb')}
data = {'device_id': device_id, 'md5': md5_checksum}

upload_response = requests.post(upload_url, files=files, data=data)

print(upload_response.status_code)
print(upload_response.json())

