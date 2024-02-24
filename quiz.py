import PySimpleGUI as sg
import random
import json
import os

sg.theme('DarkBlue3')

def load_questions_from_json():
    try:
        with open('quiz_questions.json', 'r') as file:
            questions = json.load(file)
    except FileNotFoundError:
        return []
    return questions

def delete_questions_json_file():
    try:
        os.remove('quiz_questions.json')
        print("Deleted quiz_questions.json file")
    except FileNotFoundError:
        print("quiz_questions.json file not found")    

quiz_layout = [
    [sg.Text('Quiz Time!')],
    [sg.Text('Select the correct answer for each question')],
    [sg.Text('', size=(30,1), key='question')],
    [sg.Listbox([], size=(30, 4), key='answers'),
     sg.Text('Score: 0', key='score', visible=False)],
    [sg.Button('Next'), sg.Button('Quit'), sg.Button('Reveal Correct Answer', key='reveal', visible=False)]
]

quiz_window = sg.Window('Quiz - Quiz', quiz_layout, finalize=True)

def save_questions_to_json(questions):
    with open('quiz_questions.json', 'w') as file:
        json.dump(questions, file)

questions = load_questions_from_json()

question_index = 0
score = 0
start_quiz = False
reveal = False

while True:
    current_question = questions[question_index]
    correct_answer = current_question[1]
    wrong_answers = current_question[2]
    answers = random.sample([correct_answer] + wrong_answers, len(wrong_answers) + 1)

    quiz_window['question'].update(current_question[0])
    quiz_window['answers'].update(values=answers)
    quiz_window['score'].update(f'Score: {score}', visible=start_quiz)
    quiz_window['reveal'].update(visible=reveal)

    event, values = quiz_window.read()

    if event == sg.WIN_CLOSED or event == 'Quit':
        break

    if start_quiz:
        if event == 'Next':
            if values['answers']:
                if values['answers'][0] == correct_answer:
                    score += 1
            else:
                sg.popup('Please select an answer')
                continue

            question_index += 1

            if question_index < len(questions):
                reveal = False
            else:
                reveal = True
        elif event == 'Reveal Correct Answer':
            reveal = True

        if not reveal and question_index < len(questions):
            quiz_window['score'].update(f'Score: {score}', visible=True)
        else:
            sg.popup(f'Quiz completed! Your score: {score}/{len(questions)}')
            delete_questions_json_file()
            break
    else:
        start_quiz = True

quiz_window.close()
