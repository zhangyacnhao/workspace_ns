import requests
import json

url = "http://192.168.29.238:11434/api/generate"
data = {
    #"model": "test:v1.0",
    #"model": "qwen2-1.5b-chat-mul_01_q4_0.gguf:v1.0",
    "model": "qwen2-1.5b-chat-hf-mul_01.gguf:v1.0",
    "prompt": "如何成为一名算法工程师"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    json_lines = response.text.strip().split('\n')
    
    total_tokens = 0
    eval_count = 0
    eval_duration = 0
    
    for line in json_lines:
        json_data = json.loads(line)
        if "eval_count" in json_data and "eval_duration" in json_data:
            eval_count = json_data["eval_count"]
            eval_duration = json_data["eval_duration"]
        total_tokens += 1
    
    if eval_count > 0 and eval_duration > 0:
        tokens_per_second = eval_count / (eval_duration * 10** -9)
        print(f"每秒生成的令牌数: {tokens_per_second:.2f} token/s")
    else:
        print("无法计算每秒生成的令牌数，eval_count或eval_duration无效。")
else:
    print(f"请求失败，状态码: {response.status_code}")

