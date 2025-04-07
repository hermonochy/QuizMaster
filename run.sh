source venv/bin/activate || ./setup.sh
echo "Activated virual enviroment..."
echo "Fetching Quizzes..."
cd Quizzes && git pull && cd ../ || echo "Unable to update..."
echo "Running QuizMaster..."
./quiz.py || (./setup.sh && ./quiz.py)
