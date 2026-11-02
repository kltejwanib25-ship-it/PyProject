@echo off
setlocal
cd /d "%~dp0"
.venv\Scripts\python.exe build_windows.py %*
if errorlevel 1 (
 echo Build failed. Read the error above.
 pause
 exit /b 1
)
pause
