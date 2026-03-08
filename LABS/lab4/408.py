import math

class PrimeNumbers:
    def __init__(self, num):
        self.num = num

    def func(self):
        for value in range(2, self.num + 1):
            found = True
            for i in range(2, int(math.sqrt(value)) + 1):
                if value % i == 0:
                    found = False
                    break
            if found:
                print(value, end=" ")

num = int(input())
cl = PrimeNumbers(num)
cl.func()
