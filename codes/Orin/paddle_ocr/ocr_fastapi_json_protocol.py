#fastapi
from fastapi import FastAPI, Form
import uvicorn
import base64


import os
from paddleocr import PaddleOCR, draw_ocr
import numpy as np

import re

ocr = PaddleOCR(lang="ch", enable_mkldnn=False, show_log=False, warmup=True, use_angle_cls=False, 
                det_model_dir='./ch_PP-OCRv3_det_slim_infer',
                rec_model_dir='./ch_PP-OCRv3_rec_slim_infer',
                cls_model_dir='./ch_ppocr_mobile_v2.0_cls_infer',
                det_db_thresh=0.2,
                det_db_box_thresh=0.4,
                det_limit_side_len=960)

ocr.ocr(np.random.randint(0,255,size=(480,960,3)))

app = FastAPI()

from fastapi import File, UploadFile, Form
import cv2

@app.post("/predict_ocr")
#async def ocr_aiqiyi(file: UploadFile = File(...)):
def ocr_aiqiyi(image: str=Form(...)):
    ret_dict ={"message":"predict_ocr","results":[], "status":-1} # status -1 表示 异常，0表示正常执行
    try:
        img = base64.b64decode(image)
        srcImg = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
        srcImg = srcImg[:,:,:3]

        result = ocr.ocr(srcImg)
        result = result[0]
    
        for line in result:
            confidence = line[1][1]
            text = line[1][0]
            text_region = list(line[0])
            ret_dict["results"].append({"confidence":confidence,"text":text,"text_region":text_region})
        ret_dict["status"]=0
    except:
        ret_dict ={"message":"predict_ocr","results":[],"status":-1}
    return ret_dict


@app.post("/bool_aiqiyi_advertising")
# async def bool_advertising(file: UploadFile = File(...)):
#     contents = await file.read()
#     srcImg = cv2.imdecode(np.frombuffer(contents, np.uint8), -1)  
def bool_advertising(image:str=Form(...)):
    ret_dict={"message":"bool_advertising","content":0,"status":-1} # content:0表示无广告，1表示有广告; status -1 表示异常， 0表示正确执行
    try:
        img = base64.b64decode(image)
        srcImg = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
        srcImg = srcImg[:,:,:3]

        result = ocr.ocr(srcImg[0:srcImg.shape[0] // 5:, srcImg.shape[1] //2:srcImg.shape[1], :])
        result = result[0]
        txts = [line[1][0] for line in result]

        bBackKey = False
        badv = False
        
        for txt in txts:
            if '返回键' in txt:
                bBackKey = True
            if '关闭广告' in txt:
                badv = True
            if bBackKey and badv:
                ret_dict["content"] = 1
                break
                #return ret_dict
        ret_dict["status"] = 0
    except:
        ret_dict={"message":"bool_advertising","content":0,"status":-1} # content:0表示无广告，1表示有广告; status -1 表示异常， 0表示正确执行
    return ret_dict

@app.post("/get_aiqiyi_processbar_curtime")
# async def get_aiqiyi_processbar_curtime(file: UploadFile = File(...)):
#     contents = await file.read()
#     srcImg = cv2.imdecode(np.frombuffer(contents, np.uint8), -1)  
def get_aiqiyi_processbar_curtime(image:str=Form(...)):
    ret_dict ={"message":"processbar_curtime", "cur_time":0, "status":-1} # cur_time 当前时间（s）, status 0:没检测到时间 1:检测成功,-1 执行异常
    try:
        img = base64.b64decode(image)
        srcImg = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
        srcImg = srcImg[:,:,:3]


        result = ocr.ocr(srcImg[srcImg.shape[0] * 2 // 3:,:,:])
        result = result[0]
        txts = [line[1][0] for line in result]

        pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2})/(\d{2}):(\d{2}):(\d{2})')
        
        result = None
        for txt in txts:
            result = pattern.match(txt)
            if result is not None:
                break
        if result is None:
            ret_dict["status"]=0
        else: 
            ch,cm,cs =int(result.group(1)),int(result.group(2)),int(result.group(3))
            
            cur_time = ch*60*60 + cm*60 + cs
            
            ret_dict["cur_time"] = cur_time
            ret_dict["status"]= 1
    except:
        ret_dict ={"message":"processbar_curtime", "cur_time":0, "status":-1} # cur_time 当前时间（s）, status 0:没检测到时间 1:检测成功,-1 执行异常
    
    return ret_dict

'''
@param Img: 输入图片,（爱奇艺视频播放中，连续两次按下向下按键后的截图: adb shell screencap -p /sdcard/screenshot.png）
@return: 找到的当前集数，如果没有找到当前集数，返回None
@author: lyon 2024-07-03
'''
@app.post("/get_aiqiyi_current_episode")
def choose_episode(image:str=Form(...)):
    ret_dict = {"message":"current_episode", "current_episode":0, "status":-1} # status -1: 错误，0: 没有检测到当前集，1: 检测到当前集
    try:
        img = base64.b64decode(image)
        srcImg = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
        srcImg = srcImg[:,:,:3]

        result = ocr.ocr(srcImg)
        result = result[0]

        core_xy_dict = {}
        mean_y = 0
        cnt = 0
        for line in result:
            if line[1][0].isdigit():
                core_xy = np.array(line[0]).mean(axis=0)
                core_xy_dict[line[1][0]] = core_xy
                mean_y += core_xy[1]
                cnt += 1

        if cnt == 0:
            ret_dict["status"] = 0
            return ret_dict

        mean_y /= cnt

        core_xy_dict_filter = {}
        for key, value in core_xy_dict.items():
            if abs(value[1] - mean_y) < 50:
                core_xy_dict_filter[key] = value

        if len(core_xy_dict_filter) == 0:
            ret_dict["status"] = 0
            return ret_dict
        
        key_list = list(map(int, core_xy_dict_filter.keys()))
        value_list = [ value[0] for value in core_xy_dict_filter.values()]

        min_v = 100000
        max_v = 0
        
        for key in key_list:
            if int(key) < min_v:
                min_v = int(key)
            if int(key) > max_v:
                max_v = int(key)        

        step_stride = 185
        if len(core_xy_dict_filter) == 1:
            key_list.append(key_list[0] + 1)
            value_list.append(value_list[0] + step_stride)    
        
        start_index = 1
        end_index = 10
        if max_v - min_v >= 9:
            start_index = min_v
            end_index = max_v
        else:
            leak_cnt = 10 - (max_v - min_v)
            start_index = min_v - leak_cnt
            end_index = max_v + leak_cnt

        z = np.polyfit(key_list, value_list, 1)

        episode_idx = np.arange(start_index, end_index + 1)
        col_x = np.polyval(z, episode_idx)
        
        height, width = srcImg.shape[:2]
        max_gray_episode_idx = 0
        max_gray = 0
        mean_y = int(mean_y)
        box_width = 160
        box_height = 100
        y_start = mean_y - box_height // 2
        y_start = min(max(0, y_start), height)
        y_end = mean_y + box_height // 2
        y_end = min(max(0, y_end), height)
        for i in range(len(col_x)):
            if col_x[i] > 0 and col_x[i] < width:
                x_start = col_x[i] - box_width // 2
                x_start = round(min(max(0, x_start), width))
                x_end = col_x[i] + box_width // 2
                x_end = round(min(max(0, x_end), width))
                gray_mean = srcImg[y_start:y_end, x_start:x_end,:].mean()
                if gray_mean > max_gray:
                    max_gray = gray_mean
                    max_gray_episode_idx = i
        
        cur_episode = episode_idx[max_gray_episode_idx]
        
        if cur_episode <= 0 or max_gray < 80:
            ret_dict["status"] = 0
            return ret_dict
        
        ret_dict["status"] = 1

        ret_dict["current_episode"] = int(cur_episode)
        #return ret_dict
    except Exception as e:
        ret_dict = {"message":"current_episode", "current_episode":0, "status":-1}
    
    return ret_dict




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
