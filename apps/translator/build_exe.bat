@echo off
chcp 65001 >nul
REM 一键打包 FinancialStatementTranslator.exe
py -m pip install -r requirements.txt
py -m PyInstaller --noconfirm --clean --onefile --windowed ^
  --name FinancialStatementTranslator ^
  --add-data "glossary.json;." ^
  translator.py
echo.
echo 打包完成：dist\FinancialStatementTranslator.exe
pause
