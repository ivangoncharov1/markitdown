@echo off
rem Run watcher in a visible window (to see logs). Close window to stop.
cd /d "%~dp0"
.venv\Scripts\python watch.py
