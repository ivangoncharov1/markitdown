@echo off
rem One-time setup: venv + markitdown from this repo + autostart with Windows
cd /d "%~dp0"
py -3 -m venv .venv || python -m venv .venv || (echo Python not found & pause & exit /b 1)
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -e "..\..\packages\markitdown[all]"
if not exist .env copy /y .env.example .env >nul
notepad .env
copy /y "%~dp0start-hidden.vbs" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\markitdown-bot.vbs" >nul
echo.
echo Done. Bot will start with Windows. Starting it now...
wscript "%~dp0start-hidden.vbs"
pause
