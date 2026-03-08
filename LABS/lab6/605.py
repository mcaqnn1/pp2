import re
class Has_a_Vowel:
    def __init__ (self,txt):
        self.txt = txt

    def Result(self):
        if re.search(r"a",self.txt) or re.search(r"e",self.txt) or re.search(r"i",self.txt) or  re.search(r"o",self.txt) or re.search(r"u",self.txt) or re.search(r"A",self.txt) or re.search(r"E",self.txt) or re.search(r"I",self.txt) or  re.search(r"O",self.txt) or re.search(r"U",self.txt):
            return True
        return False
word = input()
res = Has_a_Vowel(word)
if (res.Result()):
    print("Yes")
else:
    print("No")
