#1
class num:
    x=1
p=num()
print(p.x)

#2
class people:
    def __init__(self, name, age):
        self.name=name
        self.age=age
person1=people("Mike", 22)
print(person1.name, person1.age)

#3
class students:
    def __init__(self, name, year):
        self.name=name
        self.year=year
    def info(self):
        print(self.name, self.year)
student1=students("Dina", 2)
student1.info()

#4
class addition:
    def add(self, a, b):
        return(a+b)
ex=addition()
print(ex.add(7, 9))