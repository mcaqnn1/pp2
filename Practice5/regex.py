#Напишите программу на Python, которая сопоставляет строку, содержащую символ '', за которым 'a'следует ноль или более 'b'символов ''.
import re

txt = input()
if re.fullmatch(r"ab*",txt):
    print("Yes")
else:
    print("No")


#Напишите программу на Python, которая сопоставляет строку, содержащую символ , 'a'за которым следуют два-три символа 'b'.
import re

txt = input()
if re.fullmatch(r"ab{2,3}",txt):
    print("Yes")
else:
    print("No")


#Напишите программу на Python для поиска последовательностей строчных букв, соединенных знаком подчеркивания.
import re

txt = input()
pattern = "_"
found = False
if txt.islower():
    for x in txt:
        if re.search(pattern,x):
            found = True
if found:
    print("Yes")
else:
    print("No")


#Напишите программу на Python для поиска последовательности, в которой сначала идет заглавная буква, а затем строчная.
txt = input()
if txt[0].isupper() and txt[1].islower():
    print("Yes")
else:
    print("No")


#Напишите программу на Python, которая сопоставляет строку, содержащую символ , 'a'за которым следует любой символ, заканчивающийся на 'b'.
txt = input()
if txt[0] == "a" and txt[len(txt)-1] == "b":
    print("Yes")
else:
    print("No")


#Напишите программу на Python, которая заменяет все вхождения пробела, запятой или точки двоеточием.
import re

txt = input()
txt = re.sub(r" ",",",txt)
print(txt)


#Напишите программу на Python для преобразования строки в стиле snake case в строку в стиле camel case.
import re
txt = input()
txt = re.sub(r"_"," ",txt)
txt_copy = txt.split()
res = txt_copy[0]
for word in txt_copy[1:]:
    res += " " + word.capitalize()
res_copy = res.split()
print("".join(res_copy))


            
