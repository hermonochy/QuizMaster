import pytest

from modules.persistence import load_quiz,NoQuizTitleException

def test_load_nonexistingfile_fails():
    quiz = load_quiz("testdata/testquizNotExisting.json")
    assert not quiz


def test_load_corrupted_quizfile_fails():
   with pytest.raises(NoQuizTitleException) as exceptionmessage:
        quiz = load_quiz("testdata/testquizcorrupted.json")

def test_load_first_answer():
   quiz = load_quiz("testdata/testquiz.json")
   assert quiz["listOfQuestions"][1]["correctAnswer"] == "286"

def test_load_quiz_file():
    quiz = load_quiz("testdata/testquiz.json")
    print(quiz)
    assert quiz, "File not loaded."

    quizkeylist = quiz.keys()
    
    assert 'title' in quizkeylist and 'listOfQuestions' in quizkeylist, "No quiz file"

