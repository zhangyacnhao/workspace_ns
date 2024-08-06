#!/opt/custom/bin/python3
import requests
import json
import time
import os
import ctypes
import sys
import pdb




win_ip = os.environ.get('WINIP')  
debian_ip = os.environ.get('DEBIP')  
# 检查环境变量是否存在且不为空  
if not win_ip or not debian_ip:  
    raise ValueError("环境变量 os IP 未设置或为空")  
    exit(1)



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SO_PATH = os.path.join(BASE_DIR, './', './demo_so/libsdk.so')

# Load the shared library

lib = ctypes.CDLL(SO_PATH)
lib.AIsend.argtypes = [ctypes.c_int]
lib.AIsend.restype = ctypes.c_int
lib.AIrev.argtypes = [ctypes.c_int]
lib.AIrev.restype = ctypes.c_int
lib.get_version_number.argtypes = []
lib.get_version_number.restype = ctypes.c_char_p
lib.get_gpioValue.argtypes = []
lib.get_gpioValue.restype = ctypes.c_int

def process_user_input(cmd):
    if cmd == 0:
        print("Exiting...")
        return

    elif cmd == 1:
        version = lib.get_version_number().decode() 
        print("***** get version ******")
        print(version)

    elif cmd in [2, 3, 4]:
        ret = lib.AIsend(cmd)
        print (ret)

    elif cmd == 5:
        ret = lib.AIrev(1)

    elif cmd == 6:
        gpio_value = lib.get_gpioValue()
        if gpio_value == 1:
            print(lib.AIrev(1))
        else:
            pass
            # Handle other GPIO values if necessary

    else:
        print("Invalid input. Please enter a number between 0 and 6.")


HEARTBEAT_URL_win = "http://" + win_ip + ":8088/api/heartbeat"
HEARTBEAT_URL_deb = "http://" + debian_ip + ":8088/api/heartbeat"
REBOOT_d2wURL = "http://" + debian_ip +":8088/api/reboot/debian2win?password=1"
REBOOT_w2dURL = "http://" + win_ip + ":8088/api/reboot/win2debian"


reboot_flag = False

#pdb.set_trace()

while True:
    try:
        response = requests.get(HEARTBEAT_URL_deb, timeout=5)
        print("get 请求完成")
        response.raise_for_status()  # 如果状态不是200，将会抛出HTTPError异常
        json_response = json.loads(response.text)
        errcode = json_response.get('errcode')
        if errcode != 0:
            print("errcode 不等于0")
            print("心跳返回非预期结果，正在尝试重启...")
            process_user_input(4) # 通过gpio硬重启
            time.sleep(60)
            print("硬重启完成，开始执行进入debian重启进入windows...")
            requests.get(REBOOT_d2wURL) # 通过接口软重启从debian到win
        
            start_time = time.time()
            while True:
                print("while ture 循环5分钟或者get请求成功退出此循环")
                response = requests.get(HEARTBEAT_URL_win, timeout=5)
                json_response = json.loads(response.text)
                errcode = json_response.get('errcode')
                if (time.time() - start_time >= 3600) or (errcode == 0) :
                    time.sleep(30)
                break

    except requests.exceptions.RequestException as e:
        print("get心跳异常，进入except后正在硬重启...")
        process_user_input(4) # 通过gpio硬重启
        time.sleep(60)
        print("重启sleep 60s结束，开始执行进入debian软重启进入windows...")
        requests.get(REBOOT_d2wURL) # 通过接口软重启从debian到win
    
        start_time = time.time()
        while True:
            try:
                print("while ture 循环5分钟或者get请求成功退出此循环")
                response = requests.get(HEARTBEAT_URL_win, timeout=5)
                json_response = json.loads(response.text)
                errcode = json_response.get('errcode')
                if (time.time() - start_time >= 3600) or (errcode == 0) :
                    time.sleep(3)
                    requests.get(REBOOT_w2dURL)
                    time.sleep(10)
                    process_user_input(4)
                    time.sleep(40)
                    break
            except requests.exceptions.RequestException as e:
                #print("get心跳异常，进入except后正在硬重启...")
                pass
    print("进入循环5s后再进入外层while true循环")
    time.sleep(5)
