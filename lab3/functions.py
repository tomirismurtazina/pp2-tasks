#1
def hello():
    print("Hello, World!")
hello()

#2
def convert(kel):
    return kel-273
print(convert(0))
print(convert(400))

#3
def greet(name):
    return "Hello, "+name
name=input()
message=greet(name)
print(message)

#4
def sum(*numbers):
    total=0
    for i in numbers:
        total+=i
    return total
print(sum(1, 2, 3, 4, 5))

#5
def func(name, age):
    print("My name is "+name+"and I am "+age+" years old")
n=input()
a=input()
func(n, a)
func(name=n, age=a)

#6
def person(**char):
    print(char["fname"]+char["lname"]+" is "+char["age"]+" years old")
fname=input()
lname=input()
age=input()
person(fname, lname, age)

#7
def mult(a, b, c):
    return a*b*c
numbers=[1, 2, 3]
print(mult(*numbers))