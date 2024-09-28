import base64
import ctypes
import os.path
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import cv2 as cv
import numpy as np
import pyautogui as pt
import pygetwindow
import requests
import torch
from PIL import ImageGrab
from loguru import logger
from ultralytics import YOLO


class _log:

    def __init__(self, url: str = None):
        self.url = url

    def _sendLog(self, level, message):
        if self.url:
            requests.post(self.url, json={
                "level"  : level,
                "message": base64.b64encode(message.encode()).decode()
            })

    def debug(self, message):
        self._sendLog("DEBUG", message)

    def info(self, message):
        self._sendLog("INFO", message)

    def warning(self, message):
        self._sendLog("WARNING", message)

    def error(self, message):
        self._sendLog("ERROR", message)

    def critical(self, message):
        self._sendLog("CRITICAL", message)


def press(code, press_time: float = 0.0):
    driver.key_down(code)
    if press_time:
        time.sleep(press_time)
    driver.key_up(code)


if len(sys.argv) == 2:
    log = _log("http://localhost:60721/log")
else:
    log = _log()

model = YOLO("./best.pt")
zoom = 1
if os.path.exists(r".\ghub_device.dll"):
    driver = ctypes.CDLL(r'.\ghub_device.dll')
    if driver.device_open() != 1:
        press = pt.press
        log.info("Use pyautogui")
    else:
        log.info("Use logic dll")
else:
    press = pt.press
    log.info("Use pyautogui")

window_title = "第五人格"
window = pygetwindow.getWindowsWithTitle(window_title)
if not window:
    print("未找到窗口")
    exit(1)
window = window[0]

device = torch.device("cuda:0")
# device = torch.device("cpu")
model.to(device)
line_rect = None
key_press_time = 0

if __name__ == '__main__':
    with ThreadPoolExecutor() as pool:
        while True:
            if window:
                x, y, width, height = window.left, window.top, window.width, window.height
                x, y, width, height = x * zoom, y * zoom, width * zoom, height * zoom
                if x < 0 or y < 0:
                    continue
                screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                image_src = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
                size_x, size_y = image_src.shape[1], image_src.shape[0]
                image_det = cv.resize(image_src, (640, 320))
                result = model.predict(source=image_det, imgsz=640, conf=0.75, save=False)


            @logger.catch
            def _run():
                global key_press_time
                global image_src
                global line_rect
                raw_boxes = result[0].boxes
                raw_boxes = sorted(raw_boxes, key=lambda x: x.xywhn[0][0])
                items = {}
                for box in raw_boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]  # 假设 model.names 是类别名称列表
                    box = box.xywhn[0]
                    pt1 = (int((box[0] - box[2] / 2) * size_x), int((box[1] - box[3] / 2) * size_y))
                    pt2 = (int((box[0] + box[2] / 2) * size_x), int((box[1] + box[3] / 2) * size_y))
                    items[class_id] = {
                        "name": class_name,
                        "xywh": (pt1, pt2)
                    }
                    # 画框
                    # cv.rectangle(image_src, (int((box[0] - box[2] / 2) * size_x), int((box[1] - box[3] / 2) * size_y)),
                    #              (int((box[0] + box[2] / 2) * size_x), int((box[1] + box[3] / 2) * size_y)),
                    #              color=(255, 255, 0), thickness=2)
                    # pt.click(x=x + box[0] * size_x, y=y + box[1] * size_y)
                blue_note_rect = None
                red_note_rect = None
                for class_id, item in items.items():
                    if item["name"] == "Blue note":
                        blue_note_rect = item["xywh"]
                    elif item["name"] == "line" and not line_rect:
                        log.info("Set line successful")
                        line_rect = item["xywh"]
                    elif item["name"] == "Red note":
                        red_note_rect = item["xywh"]

                def is_overlap(rect1, rect2):
                    """检查两个矩形是否重叠"""
                    x1_min, y1_min = rect1[0]
                    x1_max, y1_max = rect1[1]
                    x2_min, y2_min = rect2[0]
                    x2_max, y2_max = rect2[1]

                    # 只要两个矩形的边界框有任何重叠的部分，就认为它们重叠
                    if x1_max >= x2_min and y1_min >= y2_min and y1_max <= y2_max:
                        return True
                    return False

                if blue_note_rect and line_rect and is_overlap(blue_note_rect, line_rect):
                    # 执行某个按键操作
                    log.info("Blue note 与 line 重叠，执行某个按键操作")
                    if time.time() - key_press_time > 0.2:
                        key_press_time = time.time()
                        color = image_det[int(320 * 0.93), int(630 * 0.96)]
                        # log.debug(str(color))
                        if color[0] < 130:
                            log.info("Press d")
                            press("d")
                        else:
                            log.info("Press f")
                            press("f")
                if red_note_rect and line_rect and is_overlap(red_note_rect, line_rect):
                    # 执行某个按键操作
                    log.info("Red note 与 line 重叠，执行某个按键操作")
                    if time.time() - key_press_time > 0.2:
                        key_press_time = time.time()
                        log.info("Press a")
                        press("a")
                # image_src = cv.resize(image_src, (640, 342))
                # cv.imshow("frame", image_src)
                # cv.resizeWindow("frame", 640, 342)
                # if cv.waitKey(1) == ord('q'):
                #     return
                # pass


            pool.submit(_run)
