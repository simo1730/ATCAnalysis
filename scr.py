import re

# open the text file and read the data
file = open("bos.txt",'r')

text = file.read()
# match a regex pattern for formatted times
# STILL HAVE TO FIND OUT, HOW TO INCLUDE DIRECTION
matches = re.findall(r'(TIMES \d+(?:\.\d+ )\d+(?:\.\d+)?)',text)

print(matches)

with open('stamps.txt', 'w') as f:
    print(matches, file=f)
    
    
    
f1=open("stamps.txt","r+")
input=f1.read()
print(input)
input=input.replace(',','\n')
input=input.replace('TIMES','')
input=input.replace("'","")
input=input.replace("[","")
input=input.replace("]","")
print(input)
f2=open("stampsfromatted.txt","w+")
f2.write(input)
f1.close()
f2.close()