import re
f=open("raw.txt", "r", encoding="utf-8")
c=f.read()
prices=re.findall("[0-9]+\s[0-9]+,00|[0-9]+,00", c)
names=re.findall(r"\d+\.\n(.+)", c)
sum=prices[-2]
date=re.search("Время:\s[0-9]{2}.[0-9]{2}.[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}", c)
payment=re.search("Банковская карта", c)
print(*prices)
print(*names)
print(sum)
print(date.group())
print(payment.group())