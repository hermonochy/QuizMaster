@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing requirements in virtual environment...
pip install -r requirements.txt

echo Deactivating virtual environment...
deactivate

echo Done!
