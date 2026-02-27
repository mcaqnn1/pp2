#Создайте генератор, который генерирует квадраты чисел до некоторого значения N.
def SquaresOfNumbers(num):
    for i in range(num + 1):
        yield i * i

num = int(input())
g = SquaresOfNumbers(num)
for x in g:
    print(x, end=" ")


#Напишите программу, использующую генератор, для вывода четных чисел.
def function(num):
    for i in range(num + 1):
        if i % 2 == 0:
            yield i
num = int(input())
h = function(num)

print(",".join(str(x) for x in function(num)))


#Определите функцию с генератором, которая может перебирать числа, делящиеся на 3 и 4, в заданном диапазоне от 0 до n.
def function(num):
    for i in range(num + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
num = int(input())

j = function(num)

for x in j:
    print(x,end=" ")


#Реализуйте генератор, который будет squaresвыдавать квадраты всех чисел от (a) до (b).
def squaresA_B(a,b):
    for i in range(a,b + 1):
        yield i * i
a,b = map(int,input().split())

f = squaresA_B(a,b)
for x in f:
    print(x,end=" ")


#Реализуйте генератор, который возвращает все числа от (n) до 0.
def function(num):
    for i in range(num,0,-1):
        yield i
    
num = int(input())
d = function(num)
for x in d:
    print(x,end=" ")
