#1
def square(n):
    for i in range(1, n):
        yield i**2
n=int(input())
l=square(n)
for k in l:
    print(k)

#2
def even(n):
    for i in range(n+1):
        if i%2==0:
            yield i
n=int(input())
l=list(even(n))
print(*l, sep=", ")

#3
def div(n):
    for i in range(n):
        if i%3==0 or i%4==0:
            yield i
n=int(input())
l=div(n)
for k in l:
    print(k)

#4
def squares(a,b):
    for i in range(a, b):
        yield(i**2)
a=int(input())
b=int(input())
l=squares(a, b)
for k in l:
    print(k)

#5
def nums(n):
    while n>0:
        yield n
        n-=1
n=int(input())
l=list(nums(n))
print(*l)