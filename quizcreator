#!/usr/bin/env python3
import modules.PySimpleGUI as sg
import json
from modules.persistence import QuizQuestion


questionList = []

mainWinowLayout = [
        [sg.Text("Title of Quiz:"), sg.InputText(key='quiz_name')],
        [sg.Listbox(questionList,size = (125,25), key='quizquestionentry',enable_events = True), sg.Text(key='textbox',size = (20,10))],
        [sg.Button('Open'), sg.Button('Save'), sg.Button("Edit Question"), sg.Button("Add Question"), sg.Button("Delete Question")],
        [sg.Button('Quit')]
    ]
    
    

mainWindow = sg.Window('Quiz Creator', mainWinowLayout)

def make_questionEditorWindow():
    questionEditorLayout = [
            [sg.Text('Enter the question:'), sg.InputText(key='question')],
            [sg.Text('Enter the correct answer:'), sg.InputText(key='correct_answer')],
            [sg.Text('Enter the wrong answers:'), sg.InputText(key='wrong_answers')],
            [sg.Text('Enter the time given to awnser:'), sg.InputText(key = 'time_given')],
            [sg.Checkbox("Have music playing", default=True, key = "checkbox_play_music",enable_events = True)],
            [sg.Button('Add'), sg.Button('Cancel')]
        ]
        
    questionEditorWindow = sg.Window('Question Editor', questionEditorLayout, finalize = True)
    return questionEditorWindow

while True:
   event,values = mainWindow.read()
   
   if event == 'quizquestionentry':
     if len(values['quizquestionentry'])>0:
         answers = ("correct awnser:",values['quizquestionentry'][0].correctAnswer, "wrong awnsers:",values['quizquestionentry'][0].wrongAnswers)
         outputtext = "Correct answer: \n" + answers[1]+ "\n Wrrong answers:\n" + str(answers[3]) 
         mainWindow["textbox"].update(outputtext) 
    
   if event == sg.WIN_CLOSED or event == 'Quit':
        print("Bye...")
        break

   if event == 'Edit Question':
      try:
        index = int(''.join(map(str, mainWindow["quizquestionentry"].get_indexes())))
        quizQuestion = questionList[index]
      except ValueError:
        sg.Popup("Select a message to edit!")  
        continue

      questionEditorWindow = make_questionEditorWindow()
      questionEditorWindow['question'].update(quizQuestion.question)
      questionEditorWindow['correct_answer'].update(quizQuestion.correctAnswer)
      questionEditorWindow['wrong_answers'].update(''.join((','+str(e)) for e in quizQuestion.wrongAnswers)[1:])
      questionEditorWindow['time_given'].update(quizQuestion.timeout)
      questionEditorWindow['checkbox_play_music'].update(quizQuestion.playMusic)
      editorEvent,editorValues = questionEditorWindow.read()
      if editorEvent == 'Add':
          question = editorValues['question']
          correct_answer = editorValues['correct_answer']
          wrong_answers = editorValues['wrong_answers'].split(',')
          newquestion = QuizQuestion(question, correct_answer, wrong_answers, int(editorValues['time_given']))
          questionList[index]=newquestion  
          questionEditorWindow.close()
          mainWindow["quizquestionentry"].update(questionList)                            
      if editorEvent == 'Cancel':
         questionEditorWindow.close()

   if event == 'Add Question':
        questionEditorWindow = make_questionEditorWindow()
        editorEvent,editorValues = questionEditorWindow.read()
        if editorEvent == 'Add':
            question = editorValues['question']
            correct_answer = editorValues['correct_answer']
            wrong_answers = editorValues['wrong_answers'].split(',')
            try:
                time_given = int(editorValues['time_given'])
            except ValueError:
                time_given = 10
            play_music = editorValues['checkbox_play_music']
            print(f"Saving play_music: {checkbox_play_music}")
            newquestion = QuizQuestion(question, correct_answer, wrong_answers, time_given, play_music)
            questionList.append(newquestion) 
            questionEditorWindow.close()
            mainWindow["quizquestionentry"].update(questionList)                            
        if editorEvent == 'Cancel':
           questionEditorWindow.close()
        
   if event == 'Save':         
      filename = sg.popup_get_file('', save_as=True, no_window=True,initial_folder="quizzes", \
            file_types=(("All JSON Files", "*.json"),("All Files", "*.*")))
      with open(f'{filename}', 'w') as file:
         savedData = {"title": values['quiz_name'] , "listOfQuestions": questionList, "time given": editorValues['time_given']}
         print("aveddata:", savedData)
         json.dump(savedData, file, default = vars)      
         
         
   if event == 'Open':
     try:
        filename = sg.popup_get_file("Open quiz", initial_folder="quizzes",no_window=True)
        with open(filename, 'r') as file:
           quizDicts = json.load(file)
           questionList = []
           for q in quizDicts["listOfQuestions"]:
               qq = QuizQuestion(**q)
               questionList.append(qq)
           mainWindow["quizquestionentry"].update(questionList)
           titleofquiz = quizDicts["title"]
           mainWindow["quiz_name"].update(titleofquiz)
           
     except TypeError:
        ...    
                 
   if event == 'Delete Question':
      try:
        index = int(''.join(map(str, mainWindow["quizquestionentry"].get_indexes())))
        questionList.pop(index)
      except ValueError:
        sg.Popup("Select a message to delete!")  

      mainWindow["quizquestionentry"].update(questionList)     
              
mainWindow.close()              
    
