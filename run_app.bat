@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo First run install_and_run.bat to install dependencies.
  pause
  exit /b 1
)
call .venv\Scripts\activate
py -m streamlit run app.py
pause
