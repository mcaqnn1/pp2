def display(name,gpa):
    return f"Student: {name}, GPA: {gpa}"
name, gpa = input().split()
print(display(name,gpa))