# QuizMaster

QuizMaster is a fun game testing your knowledge and cognitive ability in many different areas. 
If you know how to copy and paste text to the command line interface, and can copy or clone this repository, then you're in.
If you've got some useful knowlege on top of this, you can create a quiz on it with `QuizCreator` and create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

## Usage

### Installation

##### Either:

1. Clone this repository `git clone https://github.com/hermonochy/QuizMaster`
2. Enter the directory containing the game executable: `cd QuizMaster`

##### Or:

1. Download the Zip file
2. Extract the Zip file
3. Enter the directory

##### Then Either:

Run the included script `./setup.sh` (Linux) or `setup.bat` script for Windows (known issues with msys2 python conflict, only worry about this if you are C++ dev). These scripts may take some time to complete.

##### Or: (Advanced, Ubuntu/Debian only):

1. Set up a new virtual environment: `python3 -m venv venv`
2. Activate the environment: `source venv/bin/activate`
3. Install tkinter: `sudo apt-get install python3-tk`
4. Install packages in `requirements.txt`: `pip3 install -r requirements.txt`

*Note: Steps 1 and 2 are optional, but recommended.*

### Quiz Game

In a command line window, enter `./run.sh` to start the code in Linux, or `run.bat` for Windows. Press either `Play a Quiz` or `Make a Quiz` in the homepage. `Make a Quiz` will open QuizCreator, `Play a Quiz` will allow you to search a quiz to play! You can either press the number allocated to the answer or, if you don't have a keyboard, click on the answer. Remember, you have a time limit!

![](images/QM1.png)

 At the end it will give advice appropriate to the score. Scores greater than 80& are above average, between 80% and 40% is average and less than 40% is terrible.

 ![](images/QM4.png)

 
There is a preferences window where you can change the song, volume and background colour:

![](images/QM5.png)

### Quiz Creator

![](images/QM2.png)

1. Run quizcreator by opening QuizMaster and clicking `Make a Quiz`. You can also start it separately with `./quizcreator` on the command line interface in Linux.
2. Use it to manage and create quiz questions. The `Add` button can add questions. As it is multiple choice, you need to give a correct answser and a set of wrong answers, seperated by commas. Adding the time limit is optional, in the format of an integer number of seconds. The average is 10 - 20 seconds. Afterwards, save it in an apropriate folder. A common mistake made by many users is to leave the question editor window open, which blocks QuizCreator.


## QuizMasterMini
 [QuizMasterMini](https://github.com/hermonochy/QuizMasterMini) is a smaller version of the application, made for smaller devices or people on a budget with data volumes.

## Features

### Quiz Game:
- Timed quiz questions with countdown.
- Ability to answer questions and receive scores.
- Background music during gameplay.
- Start QuizCreator
- Change settings

### Quiz Creator:
- Add, Edit, Delete, Save, Load functions for quiz questions.
- Interactive GUI interface for managing quiz questions.

Enjoy the combined functionalities of creating quizzes and playing quiz games with the Quiz Creator and Quiz Game applications provided in this code! Please add some extra quizzes for others. This repository is open to pull requests.
*Note: Many of the example quizzes are AI or teenage schoolchildren written, so may contain incorrect information.*

## Future Work

- more methods of answering questions
- adding pictures to questions
- more user friendly method of installing the game
- multiplayer options
- different game modes
- web app option
- Add links to external sources
