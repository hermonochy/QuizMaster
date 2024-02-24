import PySimpleGUI as sg
import random
import json

sg.theme('DarkBlue3')

def create_question_window(question_num):
    layout = [
        [sg.Text(f'Question {question_num}:')],
        [sg.Text('Enter the question:'), sg.InputText(key='question')],
        [sg.Text('Enter the correct answer:'), sg.InputText(key='correct_answer')],
        [sg.Text('Enter the wrong answers separated by commas:'), sg.InputText(key='wrong_answers')],
        [sg.Button('Submit'), sg.Button('Quit')]
    ]

    return sg.Window('Quiz - Add Questions', layout)

main_layout = [
    [sg.Text('Welcome to Quiz!')],
    [sg.Text('Enter the number of questions:'), sg.InputText(key='num_questions')],
    [sg.Button('Start')]
]

window = sg.Window('Quiz', main_layout, finalize=True)

def save_questions_to_json(questions):
    with open('quiz_questions.json', 'w') as file:
        json.dump(questions, file)

def load_questions_from_json():
    try:
        with open('quiz_questions.json', 'r') as file:
            questions = json.load(file)
    except FileNotFoundError:
        return []
    return questions

questions = load_questions_from_json()

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    
    if event == 'Start':
        try:
            num_questions = int(values['num_questions'])
        except ValueError:
            sg.popup('Please enter a valid number for the number of questions')
            continue

        for i in range(num_questions):
            question_window = create_question_window(i + 1)
            
            while True:
                event, values = question_window.read()

                if event == sg.WIN_CLOSED or event == 'Quit':
                    break
                
                if event == 'Submit':
                    if values['question'] == '' or values['correct_answer'] == '' or values['wrong_answers'] == '':
                        sg.popup('Please fill in all fields before submitting')
                        continue

                    question = values['question']
                    correct_answer = values['correct_answer']
                    wrong_answers = values['wrong_answers'].split(',')
                    questions.append((question, correct_answer, wrong_answers))
                    question_window.close()
                    break
        
        save_questions_to_json(questions)
        window.close()
        break
