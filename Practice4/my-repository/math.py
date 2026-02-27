#Напишите программу на Python для преобразования градусов в радианы.
import math
num = int(input("Input degree: "))
print("Output radian: ",math.radians(num))


#Напишите программу на Python для вычисления площади трапеции.
class geometry_trapezoid:
    def __init__(self, height, first_value, second_value):
        self.height = height
        self.first_value = first_value
        self.second_value = second_value

    def calculate(self):
        S = ((self.first_value + self.second_value)/2) * self.height
        print("Expected Output: ",S)

height = float(input("Height: "))
first_value = float(input("Base, first value: "))
second_value = float(input("Base, second value: "))
geometry_trapezoid_class = geometry_trapezoid(height,first_value,second_value)

geometry_trapezoid_class.calculate()


#Напишите программу на Python для вычисления площади правильного многоугольника.
import math
class geometry_regular_polyg0n:
    def __init__(self, number_0f_sides, length0f_a_side):
        self.number_0f_sides = number_0f_sides
        self.length0f_a_sude = length0f_a_side

    def calculate(self):
        S = (self.number_0f_sides * pow(self.length0f_a_sude,2))/4 * math.tan(math.pi/self.number_0f_sides)
        S = round(S)
        print("The area of the polygon is: ",S)
number_0f_sides = float(input("Input number of sides: "))
length0f_a_side = float(input("Input the length of a side: "))
geometry_regular_polyg0n_class = geometry_regular_polyg0n(number_0f_sides,length0f_a_side)

geometry_regular_polyg0n_class.calculate()


#Напишите программу на Python для вычисления площади параллелограмма.
class geometry_parallelogram:
    def __init__(self, Length_of_base, Height_of_parallelogram):
        self.Length_of_base = Length_of_base
        self.Height_of_parallelogram = Height_of_parallelogram

    def calculate(self):
        S = self.Length_of_base * self.Height_of_parallelogram
        print("Expected Output: ",S)

Length_of_base = float(input("Length of base: "))
Height_of_parallelogram = float(input("Height of parallelogram: "))
geometry_parallelogram_class = geometry_parallelogram(Length_of_base,Height_of_parallelogram)

geometry_parallelogram_class.calculate()



