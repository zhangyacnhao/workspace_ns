import requests

action_v2=(
    " 1.{'device':'','action':'打开','position':''} "
    " 2.{'device':'','action':'关闭','position':''} "
    " 3.{'device':'','action':'调暗','position':''} "
    " 4.{'device':'','action':'调亮','position':''} "
    " 5.{'device':'','action':'调高','position':'','parameter':''} "
    " 6.{'device':'','action':'调低','position':'','parameter':''}  "
    " 7.{'action':'播放','name':'','index':'','type':''} "
    " 8.{'device':'','action':'搜索','name':''} "
    " 9.{'device':'','action':'提前打开','parameter':''} "
    " 10.{'device':'','action':'提前关闭','parameter':''} "
    " 11.{'device':'','action':'打开模式','position':'','parameter':''} "
    " 12.{'device':'','action':'关闭模式','position':'','parameter':''} "
    " 13.{'device':'','action':'静音','position':''} "
    " 14.{'device':'','action':'关闭屏幕','position':''} "
    " 15.{'device':'','action':'调至','position':'','parameter':''} "
    " 16.{'device':'','action':'暂停','position':''} "
    " 17.{'device':'','action':'继续播放','position':''} "
    " 18.{'device':'','action':'快进','position':'','parameter':''} "
    " 19.{'device':'','action':'快退','position':'','parameter':''} "
    " 20.{'device':'歌曲','action':'上一首'} "
    " 21.{'device':'歌曲','action':'下一首'} "
    " 22.{'device':'','action':'右转','position':''} "
    " 23.{'device':'','action':'左转','position':''} "
    " 24.{'device':'','action':'后转','position':''} "
    " 25.{'device':'','action':'拍照','position':''} "
    " 26.{'device':'','action':'开始语音通话','position':''} "
    " 27.{'device':'','action':'结束语音通话','position':''} "
    " 28.{'device':'','action':'开始录像','position':''} "
    " 29.{'device':'','action':'停止录像','position':''} "
    " 30.{'device':'','action':'回看','position':''} "
    " 31.{'device':'','action':'查找'}"
    " 32.{'device':'','action':'查询','position':'','parameter':''}"
    " 33.{'device':'','action':'开始清洁'}"
    " 34.{'device':'','action':'充电'}"
    " 35.{'device':'','action':'暂停清洁'}"
    " 36.{'device':'','action':'继续清洁'}"
    " 37.{'device':'','action':'关闭静音','position':''}"
    " 38.{'device':'','action':'抱怨','position':'','parameter':''}"
    " 39.{'device':'视频','action':'上一集'} "
    " 40.{'device':'视频','action':'下一集'} "
    " 41.{'device':'','action':'倍速播放','position':'','parameter':''} "
    " 42.{'device':'','action':'全屏','position':''} "
    " 43.{'device':'','action':'关闭全屏','position':''} "
    " 44.{'action':'天气','time':'','location':''} "
    " 45.{'action':'订餐','name':'','store':'','number':'','other':''} "
    " 46.{'device':'','action':'重新播放','position':'','parameter':''} "
    " 47.{'action':'照片','position':''} "
    " 48.{'device':'','action':'返回','position':''} "
    " 49.{'device':'','action':'添加收藏','position':'','parameter':''} "
    " 50.{'device':'','action':'移除收藏','position':'','parameter':''} "
    " 51.{'device':'','action':'播放收藏','position':'','parameter':''} "
    " 52.{'action':'取消任务'} "
    " 53.{'device':'','action':'随机'} "
)

sys_prompt_whitout_desc=("你是一位家庭管家，可以操控家里的电器，记住返回值必须是json, 支持的接口及格式只有以下几种："
                         +action_v2+
                         "请根据用户的请求，使用合适的1个或多个接口，请勿凭空乱造。")

def lam_fastapi_service(input_text: str):
    url = "http://192.168.29.230:11434/api/chat"
    data = {
        "model": "qwen2-1.5b-chat-mul_02-Q8_0:v1.0",
        "messages": [
            {
                "role": "system",
                "content": f"<|im_start|>system\n{sys_prompt_whitout_desc}<|im_end|>\n<|im_start|>user\n{input_text}<|im_end|>\n<|im_start|>assistant\n"
            },
            {
                "role": "user",
                "content": input_text
            },

        ],
        "stream": False,
        "max_tokens": 20,
        "temperature": 0,
        "options": {
            "stop": [
                "<|im_end|>",
                "<|im_start|>",
                "<|endoftext|>"
            ]

        }
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    print("----------------------")
    print(response.text)
    if response.status_code == 200:
        #content = response.json()["choices"][0]["message"]["content"]
        #return content
        print("================")
        print(response.json())
        print("================")
    else:
        return "error"

res=lam_fastapi_service("打开卧室灯")
print(res)
