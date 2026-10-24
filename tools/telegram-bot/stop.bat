@echo off
rem Stop background bot
wmic process where "name='pythonw.exe' and commandline like '%%telegram-bot%%'" call terminate >nul
echo Stopped.
