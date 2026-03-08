class SumofSquares:
    def __init__(self,numbers_size,numbers):
        self.numbers_size = numbers_size
        self.numbers = numbers

    def Calculate(self):
        result = 0
        for i in range(self.numbers_size):
            result += pow(self.numbers[i],2)
        print(result)
numbers_size = int(input())
numbers = list(map(int,input().split()))
cal = SumofSquares(numbers_size,numbers)
cal.Calculate()