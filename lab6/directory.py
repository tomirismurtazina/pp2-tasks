import os
import shutil
path=os.getcwd()
for i in os.listdir(path):
    print(i)
ans=[]
for i in os.listdir(path):
    if i.endswith(".txt"):
        ans.append(i)
print(*ans)
shutil.move("test.txt", "newfolder")