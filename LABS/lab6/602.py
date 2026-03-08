class  CountEvenNumbers:
    def __init__(self,numbers_size,numbers):
        self.numbers_size = numbers_size
        self.numbers = numbers
    
    def EvenNumbers(self):
        count = 0
        for i in range(self.numbers_size):
            if self.numbers[i] % 2 == 0:
                count +=1
        print(count)
numbers_size = int(input())
numbers = list(map(int,input().split()))
res = CountEvenNumbers(numbers_size,numbers)
res.EvenNumbers()