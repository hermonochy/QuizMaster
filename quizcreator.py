import PySimpleGUI as sg
from dataclasses import dataclass
from typing import List
import json

@dataclass
class QuizQuestion:
   question: str
   correctAnswer: str
   wrongAnswers: List[str]
   
   def __repr__(self):
      return self.question

question1 = QuizQuestion("What is the meaning of life?", "42", ["1","2","3","5"])
question2 = QuizQuestion("What is the word of slow in chinese?", "286", ["12","22","43","35"])

questionList = [question1,question2]

mainWinowLayout = [
        [sg.Text("Title of Quiz:"), sg.InputText(key='quiz_name')],
        [sg.Listbox(questionList,size = (100,10), key='quizquestionentry',enable_events = True), sg.Text(key='textbox',size = (20,10))],
        [sg.Button('Open'), sg.Button('Save'), sg.Button("Add Question"), sg.Button("Delete Question")],
        [sg.FileBrowse(key="-IN-")],
        [sg.Button('Quit')]
    ]
    
    

mainWindow = sg.Window('Quiz Creator', mainWinowLayout)

def make_questionEditorWindow():
    questionEditorLayout = [
            [sg.Text('Enter the question:'), sg.InputText(key='question')],
            [sg.Text('Enter the correct answer:'), sg.InputText(key='correct_answer')],
            [sg.Text('Enter the wrong answers:'), sg.InputText(key='wrong_answers')],
            [sg.Button('Add'), sg.Button('Cancel')]
        ]
        
    questionEditorWindow = sg.Window('Question Editor', questionEditorLayout)
    return questionEditorWindow

while True:
   event,values = mainWindow.read()
   
   if event == 'quizquestionentry':
         answers = ("correct awnser:",values['quizquestionentry'][0].correctAnswer, "wrong awnsers:",values['quizquestionentry'][0].wrongAnswers)
         outputtext = "Correct answer: \n" + answers[1]+ "\n Wrrong answers:\n" + str(answers[3]) 
         mainWindow["textbox"].update(outputtext) 
    
   if event == sg.WIN_CLOSED or event == 'Quit':
        print("Bye...")
        break

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
         json.dump(questionList, file, default = vars)      
         
         
   if event == 'Open':
        with open('thi.json', 'r') as file:
           questionDicts = json.load(file)
           questionList = []
           for q in questionDicts:
               qq = QuizQuestion(**q)
               questionList.append(qq)
           mainWindow["quizquestionentry"].update(questionList)
                 
   if event == 'Delete Question':
      try:
        index = int(''.join(map(str, mainWindow["quizquestionentry"].get_indexes())))
        questionList.pop(index)
      except ValueError:
        sg.Popup("Select a message to delete!")  

      mainWindow["quizquestionentry"].update(questionList)     
              
mainWindow.close()              
              
              
              
              
              
              
              
              
