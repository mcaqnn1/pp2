class  CountTruthyNumbers:
    def __init__ (self,numbers_size,numbers):
        self.numbers_size = numbers_size
        self.numbers = numbers

    def Result(self):
        count = 0
        for x in range(self.numbers_size):
            if self.numbers[x] != 0:
                count += 1
        print(count)
numbers_size = int(input())
numbers = list(map(int,input().split()))
res = CountTruthyNumbers(numbers_size,numbers)
res.Result()