class DictionaryQuerywithZip:
    def __init__(self):
        self.n = int(input())
        self.keys = input().split()
        self.values = input().split()
        self.query = input()

    def solve(self):
        d = dict(zip(self.keys, self.values))
        if self.query in d:
            print(d[self.query])
        else:
            print("Not found")
obj = DictionaryQuerywithZip()
obj.solve()
