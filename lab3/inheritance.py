#1
class people:
    def __init__(self, name, age):
        self.name=name
        self.age=age
class students(people):
    pass
person1=people("Kamil", 30)
student1=students(person1.name, person1.age)
print(person1.name, person1.age)
print(student1.name, student1.age)

#2
class animals:
    def __init__(self, species, color):
        self.species=species
        self.color=color
class pets(animals):
    def __init__(self, species, color, breed, name):
        super().__init__(species, color)
        self.breed=breed
        self.name=name
animal1=animals("tiger", "orange")
pet1=pets("dog", "brown", "poodle", "max")
print(animal1.color, animal1.species)
print(pet1.species, pet1.color, pet1.breed, pet1.name)

#3
class employees(people):
    def __init__(self, name, age, position):
        super().__init__(name, age)
        self.position=position
    def show(self):
        print(f"{self.name} is {self.age} years old and works as a {self.position}")
empl1=employees("John", 42, "manager")
empl1.show()

#4
class character:
    def __init__(self, health, level, damage):
        self.health=health
        self.level=level
        self.damage=damage
class spellcaster(character):
    def __init__(self, health, level, damage, spell_charecteristic):
        super().__init__(health, level, damage)
        self.spell_charecteristic=spell_charecteristic
class warlock(spellcaster):
    def __init__(self, health, level, damage, spell_charecteristic, patron):
        super().__init__(health, level, damage, spell_charecteristic)
        self.patron=patron
char1=character(100, 20, 25)
char2=spellcaster(100, 20, 25, "charisma")
char3=warlock(100, 20, 25, "charisma", "archfey")
print(char1.health, char1.level, char1.damage)
print(char2.spell_charecteristic)
print(char3.patron)