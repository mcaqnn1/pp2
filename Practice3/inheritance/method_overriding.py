class A:
    def hi(self): print("A")

class B(A):
    def hi(self): print("B")  # override

B().hi()