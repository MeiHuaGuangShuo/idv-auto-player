# idv-auto-player

第五人格作曲家自动演奏，基于YOLO v8n

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

# 键盘输入方式

本程序支持pyAutoGUI的输入方式，也支持G Hub的驱动输入方式，
删除`ghub_device.dll`即可使用pyAutoGUI输入方式。
