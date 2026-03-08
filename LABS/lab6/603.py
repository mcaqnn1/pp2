class IndexEachWord:
    def __init__(self,words_size,words):
        self.words_size = words_size
        self.words = words

    def Result(self):
        for i in range(self.words_size):
            print(f"{i}:{self.words[i]}",end=" ")
words_size = int(input())
words = list(map(str,input().split()))
res = IndexEachWord(words_size,words)
res.Result()