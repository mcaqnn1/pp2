with open("file1.txt","w") as file:
    file.write("Woops! I have deleted the content!\n") #метод "w" перезапишет весь файл.
    file.close()

with open("file1.txt","a") as file:
    file.write("Woops! I have deleted the content!\n") # добавит в конец файла.
    file.close()

