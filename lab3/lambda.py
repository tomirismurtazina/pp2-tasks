#1
l=lambda a: a**2
print(l(5))

#2
def func(n):
    return lambda a: a**n
cube=func(3)
print(cube(2))

#3
numbers=list(map(int, input().split()))
squared=list(map(lambda x: x**2, numbers))
print(squared)

#4
div3=list(filter(lambda k: k%3==0, numbers))
print(div3)

#5
names=input().split()
sortnames=sorted(names, key=lambda o: o[1])
print(sortnames)