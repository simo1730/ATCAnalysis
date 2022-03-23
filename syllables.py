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