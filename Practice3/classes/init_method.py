class Car:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

c = Car("Toyota", 2020)
print(c.brand, c.year)