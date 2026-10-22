@echo off
rem Stop background watcher
wmic process where "name='pythonw.exe' and commandline like '%%inbox-watcher%%'" call terminate >nul
echo Stopped.
