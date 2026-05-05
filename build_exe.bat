@echo off
chcp 65001 >nul
echo 正在清理旧的构建文件...

rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q *.spec 2>nul

echo 正在安装依赖...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo 正在使用 PyInstaller 打包单文件 EXE...

python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --onefile ^
  --name "ClassTimer_By_teacher_Ma" ^
  --add-data "assets;assets" ^
  --hidden-import PySide6.QtMultimedia ^
  main.py

echo.
echo 打包完成。
echo EXE 文件位置：
echo dist\ClassTimer_By_teacher_Ma.exe
pause
