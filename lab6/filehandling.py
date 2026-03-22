import os
import shutil
f=open("sample.txt")
print(f.read())
f.close()
f=open("sample.txt", "a")
f.write("\nVlad")
f.close()
f=open("sample.txt")
print(f.read())
shutil.copyfile("sample.txt", "copy.txt")
f.close()
os.remove("sample.txt")