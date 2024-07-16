import pygetwindow as gw
from PIL import ImageGrab
import time
from loguru import logger
from pathlib import Path

zoom = 2
activated = False
max_time = 50


def capture_window(window_title, t):
    global activated
    # 获取指定标题的窗口
    window = gw.getWindowsWithTitle(window_title)
    if not window:
        logger.error(f"[{t}/{max_time}] 窗口 '{window_title}' 未找到")
        return False

    window = window[0]
    # 激活窗口
    if not window.isActive and not activated:
        window.activate()
        activated = True
        logger.info(f"窗口 '{window_title}' 已自动激活")

    # 获取窗口的坐标
    x, y, width, height = window.left, window.top, window.width, window.height
    x, y, width, height = x * zoom, y * zoom, width * zoom, height * zoom

    # 截取窗口截图
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

    # 保存截图到文件
    now = time.strftime('%Y-%m-%d %H-%M-%S')
    file_name = f"{window_title} {now}.png"
    screenshot.save(Path("screenshots", file_name))
    logger.info(f"[{t}/{max_time}] 截图[{width}x{height}+{x}+{y}]已保存为 '{file_name}'")
    return True


if __name__ == '__main__':
    for i in range(5, 0, -1):
        logger.info(f"{i}秒后开始截图")
        time.sleep(1)
    for i in range(max_time):
        if not capture_window("第五人格", i):
            break
        time.sleep(1)
