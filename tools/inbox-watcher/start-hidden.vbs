' Runs watch.py in the background without a console window
Set sh = CreateObject("WScript.Shell")
dir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
If InStr(dir, "Startup") > 0 Then dir = sh.ExpandEnvironmentStrings("%USERPROFILE%") & "\Projects\markitdown\tools\inbox-watcher"
sh.CurrentDirectory = dir
sh.Run """" & dir & "\.venv\Scripts\pythonw.exe"" """ & dir & "\watch.py""", 0, False
