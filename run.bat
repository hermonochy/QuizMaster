@echo off

echo Activating virual enviroment and running QuizMaster...
powershell -command ".\venv\Scripts\Activate.ps1; python quiz.py"
