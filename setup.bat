@echo off

echo Creating virtual enviroment...
python -m venv venv > NUL 2>&1

echo Activating virual enviroment and installing dependencies...
powershell -command ".\venv\Scripts\Activate.ps1; pip3 install -r requirements.txt --quiet; deactivate"

echo Done!
