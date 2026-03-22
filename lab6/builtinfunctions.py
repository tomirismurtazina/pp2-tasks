from functools import reduce
#1
def double(n):
    return n*2
l=[1, 2, 3, 4, 5]
res=list(map(double, l))
print(res)

#2
even=list(filter(lambda x: x%2==0, l))
print(even)

#3
r=reduce(lambda x, y: x+y, l)
print(r)

#4
for i, j in enumerate(l):
    print(i, j)

#5
k=['a', 'b', 'c', 'd', 'e']
res=list(zip(l, k))
print(res)

#6
if isinstance(l, list):
    print("l is a list")

#7
a="1"
print(type(a))
a=int(a)
print(type(a))