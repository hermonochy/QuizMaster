from glob import glob

def search_str_in_file(file_path, word):
    with open(file_path, 'r') as file:
        content = file.read()
        if word in content:
            return file_path
            
if __name__=='__main__':
  quizfiles = glob('./quizzes/**/*.json', recursive=True)

  searchTerm = input ("Word to search: ")

  #quizfileSearchResults = [search_str(file,searchTerm) for file in quizfiles]
  quizfileSearchResults= []
  for file in quizfiles:
    if search_str_in_file(file,searchTerm):
      quizfileSearchResults.append(file)

  print("Search result:")
  print(quizfileSearchResults)
