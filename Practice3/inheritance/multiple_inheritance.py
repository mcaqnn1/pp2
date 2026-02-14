class A: 
    def hi(self): print("A")
class B: 
    def bye(self): print("B")
class C(A, B): 
    pass

c = C()
c.hi(); c.bye()