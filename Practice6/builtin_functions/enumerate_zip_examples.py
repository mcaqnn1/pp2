names = ["Arsen", "Ali", "Amina"]
scores = [90, 85, 95]

print("enumerate:") #дает индекс и значение
for i, name in enumerate(names):
    print(i, name)

print("zip:") #соединяет два списка вместе
for name, score in zip(names, scores):
    print(name, score)