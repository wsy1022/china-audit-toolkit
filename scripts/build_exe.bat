@echo off
chcp 65001 >nul
rem 在仓库根目录打包启动台：产物 launcher\dist\中国审计机关常用工具包.exe
cd /d "%~dp0.."

py -3.12 -m PyInstaller --noconfirm --clean --onefile --windowed ^
  --name "中国审计机关常用工具包" ^
  --add-data "tools.json;." ^
  --icon "docs\app.ico" ^
  --exclude-module PyQt5 --exclude-module PyQt6 ^
  --exclude-module PySide2 --exclude-module PySide6 ^
  --exclude-module matplotlib --exclude-module scipy ^
  --exclude-module pandas --exclude-module tkinter.test ^
  --distpath "launcher\dist" --workpath "launcher\build" ^
  "launcher\toolbox.py"

if errorlevel 1 (
  echo.
  echo 打包失败。
  exit /b 1
)
echo.
echo 完成：launcher\dist\中国审计机关常用工具包.exe
dir /b "launcher\dist"
