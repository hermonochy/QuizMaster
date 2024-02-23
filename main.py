import PySimpleGUI as sg
import random

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

questions = []

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
        
        window.close()
        break

quiz_layout = [
    [sg.Text('Quiz Time!')],
    [sg.Text('Select the correct answer for each question')],
    [sg.Text('', size=(30,1), key='question')],
    [sg.Listbox([], size=(30, 4), key='answers'),
     sg.Text('Score: 0', key='score', visible=False)],
    [sg.Button('Next'), sg.Button('Quit'), sg.Button('Reveal Correct Answer', key='reveal', visible=False)]
]

quiz_window = sg.Window('Quiz - Quiz', quiz_layout, finalize=True)

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
            break
    else:
        start_quiz = True

quiz_window.close()
