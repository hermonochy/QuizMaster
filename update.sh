echo Updating QuizMaster...
git pull

echo Updating QuizMaster Quizzes
cd Quizzes
git pull
cd ..

./setup.sh || echo Done!
