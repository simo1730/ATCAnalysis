#skript ktory formatuje povodny prepis komunikacie a upravi ho potrebne na extrakciu slabik a nasledne urcovanie tempa
import re

# opening .txt file and reading data
txt = open("bos.txt",'r')

log = txt.read()
# match specific regex patterns for pattern

re1 = r'(FROM F\d)'
re2 = r'(TO F\d)'
re3 = r'(TEXT[\s\S]*?TIMES)'

p = re.compile('('+re1+'|'+re2+'|'+re3+')');
matches = p.findall(log)

with open('syllablestext.txt', 'w') as f:
    for match in matches:
        print(match[0])
        print(match[0], file=f)

f1=open("syllablestext.txt","r+")
input=f1.read()
print(input)
input=input.replace('(TIMES',"")
input=input.replace('TEXT ',"")
input=input.replace(')\n',"")
input=re.sub(r'\([^)]*\)', '', input)
print(input)
f2=open("syllablestextformatted.txt","w+")
f2.write(input)
f1.close()
f2.close()

# PA = open("syllablestextformatted.txt",'r')
# match = re.findall(r'FROM F1(.*?)TO F1', PA).group(1)
# print (match.group(1))

with open("syllablestextformatted.txt","r",encoding="utf-8") as f:
     PA=f.read()
     match = re.findall(r'FROM F1(.*?)TO F1', PA).group(1)
     print (match.group(1))