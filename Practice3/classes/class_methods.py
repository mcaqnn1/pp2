class User:
    count = 0

    def __init__(self, name):
        self.name = name
        User.count += 1

    @classmethod
    def total(cls):
        return cls.count

u1 = User("A")
u2 = User("B")
print(User.total())