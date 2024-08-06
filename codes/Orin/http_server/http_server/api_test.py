import requests
import hashlib

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# 设置上传文件的路径和设备ID
file_path = '/mnt/NFS1/zhangyanchao/lianbao/ai/http_server/test.jpeg'
device_id = '12345'

# 计算文件的MD5校验码
md5_checksum = calculate_md5(file_path)

# 设置上传的URL
url = 'http://192.168.29.59:11435/upload'

# 准备请求数据
files = {'image': open(file_path, 'rb')}
data = {'device_id': device_id, 'md5': md5_checksum}
#data = {'device_id': device_id}

# 发送POST请求
response = requests.post(url, files=files, data=data)

# 打印响应结果
print(response.status_code)
print(response.json())
