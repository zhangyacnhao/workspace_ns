import requests

url = "http://192.168.29.204:11434/api/generate"
payload = {
    "model": "Qwen2-7B-Instruct-q4_0.gguf:v1.0",
    "prompt": "如何成为一名算法工程师",
    "stream": False
}
response = requests.post(url, json=payload)
print(response.json())
