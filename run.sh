source venv/bin/activate --quiet
echo "Activated virual enviroment..."
echo "Attempting update..."
git pull || echo "Unable to update..."
echo "Running QuizMaster..."
./quiz.py
