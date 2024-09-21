from glob import glob

def search_str(file_path, word):
    with open(file_path, 'r') as file:
        content = file.read()
        if word in content:
            return file_path
            

quizfiles = glob('./quizzes/**/*.json', recursive=True)

searchTerm = input ("Word to search: ")

#quizfileSearchResults = [search_str(file,searchTerm) for file in quizfiles]
quizfileSearchResults= []
for file in quizfiles:
  if search_str(file,searchTerm):
    quizfileSearchResults.append(file)

print("Search result:")
print(quizfileSearchResults)
