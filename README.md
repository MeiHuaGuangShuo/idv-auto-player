# idv-auto-player

第五人格作曲家自动演奏，基于YOLO v8n，支持破译自动校准和技能自动校准

# best.pt 模型注意事项

有多人反馈出现模型损坏，现在贴上正常模型的md5和sha256

| HashType | Hash |
| :---: | :---: |
| md5 | 202f3a8ccf613402d157b943459b79cc |
| sha256| aa476d635e05d1a61f368a179deb77b86d2220b75c995d51553b90853bbf5e7c |

# 怎么使用

1. 克隆本项目

    ```shell
    git clone https://github.com/MeiHuaGuangShuo/idv-auto-player.git
    ```

   或者通过`ssh`克隆

    ```shell
    git clone git@github.com:MeiHuaGuangShuo/idv-auto-player.git
    ```

2. 安装依赖包

    ```
    pip install -r requirements.txt
    ```

    > torch 预发布版本，支持 CUDA 12.4，可安装完成后卸载 torch 相关组件后安装
    > ```shell
    > pip install --pre torch==2.5.0.dev20240713+cu124 torchvision --index-url https://download.pytorch.org/whl/nightly/cu124
    > ```

3. 运行`main.py`

    ```shell
    python main.py
    ```

   可以使用任意参数将程序设置为输出日志模式，如

    ```shell
    python main.py --log
    ```

   或者

    ```shell
    python main.py 114514
    ```

   等，只需要传入的参数有`1`个即可。

   debug控制台服务端在另一个项目[debug_server.py](https://github.com/MeiHuaGuangShuo/php_debug_console/blob/main/debug_server.py)中

## 注意事项

游戏窗口最好16:9，尽管程序会自动调节窗口大小，但是还是建议尽量接近。
使用[sizer](https://www.brianapps.net/sizer)可一键调节（记得使用管理员权限运行）

建议2速游玩，3速概率漏键，一般不会漏多于3个

模型后续不再优化（增加训练集了以后识别率下降了是真绷不住了）

# 键盘输入方式

本程序支持 `pyAutoGUI` 的输入方式，也支持 `G Hub` 的驱动输入方式，
删除 `ghub_device.dll` 即可使用pyAutoGUI输入方式。
