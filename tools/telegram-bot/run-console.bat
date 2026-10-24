@echo off
rem Run bot in a visible window (to see logs). Close window to stop.
cd /d "%~dp0"
.venv\Scripts\python bot.py
