import pygetwindow as gw
from PIL import ImageGrab
import time

zoom = 2


def capture_window(window_title):
    # 获取指定标题的窗口
    window = gw.getWindowsWithTitle(window_title)
    if not window:
        print(f"窗口 '{window_title}' 未找到")
        return False

    window = window[0]
    # 激活窗口
    if not window.isActive:
        window.activate()

    # 获取窗口的坐标
    x, y, width, height = window.left, window.top, window.width, window.height
    x, y, width, height = x * zoom, y * zoom, width * zoom, height * zoom
    print(x, y, width, height)

    # 截取窗口截图
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

    # 保存截图到文件
    now = time.strftime('%Y-%m-%d %H-%M-%S')
    file_name = f"{window_title} {now}.png"
    screenshot.save(file_name)
    print(f"截图[{width}x{height}+{x}+{y}]已保存为 '{file_name}'")
    return True


if __name__ == '__main__':
    for i in range(5, 0, -1):
        print(f"{i}秒后开始截图")
        time.sleep(1)
    for _ in range(50):
        capture_window("第五人格")
        time.sleep(1)
