' Runs bot.py in the background without a console window
Set sh = CreateObject("WScript.Shell")
dir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
If InStr(dir, "Startup") > 0 Then dir = sh.ExpandEnvironmentStrings("%USERPROFILE%") & "\Projects\markitdown\tools\telegram-bot"
sh.CurrentDirectory = dir
sh.Run """" & dir & "\.venv\Scripts\pythonw.exe"" """ & dir & "\bot.py""", 0, False
