import PySimpleGUI as sg
import json
from modules.persistence import QuizQuestion


questionList = []

mainWinowLayout = [
        [sg.Text("Title of Quiz:"), sg.InputText(key='quiz_name')],
        [sg.Listbox(questionList,size = (100,10), key='quizquestionentry',enable_events = True), sg.Text(key='textbox',size = (20,10))],
        [sg.Button('Open'), sg.Button('Save'), sg.Button("Edit Question"), sg.Button("Add Question"), sg.Button("Delete Question")],
        [sg.Button('Quit')]
    ]
    
    

mainWindow = sg.Window('Quiz Creator', mainWinowLayout)

def make_questionEditorWindow():
    questionEditorLayout = [
            [sg.Text('Enter the question:'), sg.InputText(key='question')],
            [sg.Text('Enter the correct answer:'), sg.InputText(key='correct_answer')],
            [sg.Text('Enter the wrong answers:'), sg.InputText(key='wrong_answers')],
            [sg.Text('Enter the time given(seconds):'), sg.InputText(key='time_given')],
            [sg.Text('Enter the marks given:'), sg.InputText(key='marks_given')],
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
      editorEvent,editorValues = questionEditorWindow.read()
      if editorEvent == 'Add':
          question = editorValues['question']
          correct_answer = editorValues['correct_answer']
          wrong_answers = editorValues['wrong_answers'].split(',')
          newquestion = QuizQuestion(question, correct_answer, wrong_answers)
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
            newquestion = QuizQuestion(question, correct_answer, wrong_answers)
            questionList.append(newquestion) 
            questionEditorWindow.close()
            mainWindow["quizquestionentry"].update(questionList)                            
        if editorEvent == 'Cancel':
           questionEditorWindow.close()
        
   if event == 'Save':         
      filename = sg.popup_get_file('', save_as=True, no_window=True, \
            file_types=(("All JSON Files", "*.json"), ("All Files", "*.*")))
      with open(f'{filename}', 'w') as file:
         savedData = {"title": values['quiz_name'] , "listOfQuestions": questionList}
         json.dump(savedData, file, default = vars)      
         
         
   if event == 'Open':
     try:
        filename = sg.popup_get_file("Open quiz", no_window=True)
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
    
