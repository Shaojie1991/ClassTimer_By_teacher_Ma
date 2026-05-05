# ClassTimer By teacher Ma / 做题倒计时

一个面向 Windows 10 / Windows 11 课堂投屏使用的 PySide6 桌面倒计时软件。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 打包 EXE

单文件 EXE：

```bat
build_exe.bat
```

如果单文件模式下音频播放不稳定，可以使用 onedir 版本：

```bat
build_exe_onedir.bat
```

## 功能

- 始终置顶，适合课堂投屏。
- 快捷设置 3 分钟、5 分钟、8 分钟、10 分钟、15 分钟、80 分钟、90 分钟。
- 自定义时间只保留“分”和“秒”，支持鼠标悬停滚轮调整，也支持键盘直接输入。
- 开始后进入专注模式，只显示圆形倒计时。
- 鼠标移动到窗口上方或双击窗口，可临时显示控制栏。
- 白色 / 黑色主题切换，并自动记住上次主题。
- 倒计时结束后播放 `assets/cat.mp3` 小猫提示音，支持软件内音量调节并自动保存。
