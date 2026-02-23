import datetime

#1
n=datetime.datetime.now()
d=datetime.timedelta(days=5)
k=n-d
print(k.strftime("%x"))

#2
i=datetime.timedelta(days=1)
y=n-i
t=n+i
print(y.strftime("%x"))
print(n.strftime("%x"))
print(t.strftime("%x"))

#3
print(n.strftime("%d.%m.%Y %H:%M:%S"))

#4
print((n-y).total_seconds())