class DotProduct:
    def __init__(self,n,numbers_first,numbers_second):
        self.n = n
        self.numbers_first = numbers_first
        self.numbers_second = numbers_second

    def Result(self):
        res = 0
        for i in range(n):
            res += (numbers_first[i] * numbers_second[i])
        print(res)
n = int(input())
numbers_first = list(map(int,input().split()))
numbers_second = list(map(int,input().split()))
res = DotProduct(n,numbers_first,numbers_second)
res.Result()