import requests
import hashlib
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
file_path = 'test.jpeg'
device_id = '12345'
md5_checksum = calculate_md5(file_path)
url = 'http://127.0.0.1:11435/upload'
files = {'image': open(file_path, 'rb')}
data = {'device_id': device_id, 'md5': md5_checksum}
response = requests.post(url, files=files, data=data)
print(response.status_code)
print(response.json())
