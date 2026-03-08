s = input().split()

class E:
    def __init__(self, n, b): self.n, self.b = n, b
    def t(self): return float(self.b)

class M(E):
    def __init__(self, n, b, p): super().__init__(n, b); self.p = p
    def t(self): return self.b * (1 + self.p/100)

class D(E):
    def __init__(self, n, b, k): super().__init__(n, b); self.k = k
    def t(self): return self.b + self.k*500

emp = M(s[1], int(s[2]), int(s[3])) if s[0]=="Manager" else D(s[1], int(s[2]), int(s[3])) if s[0]=="Developer" else E(s[1], int(s[2]))
print(f"Name: {emp.n}, Total: {emp.t():.2f}")
