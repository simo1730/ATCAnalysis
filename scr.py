import re

# opening .txt file and reading data
txt = open("bos.txt",'r')

log = txt.read()
# match specific regex patterns for formated time

re1 = r'(FROM F\d)'
re2 = r'(TO F\d)'
re3 = r'(TIMES \d+(?:\.\d+ )\d+(?:\.\d+)?)'

p = re.compile('('+re1+'|'+re2+'|'+re3+')');
matches = p.findall(log)


with open('stamps.txt', 'w') as f:
    for match in matches:
        print(match[0])
        print(match[0], file=f)
    
    
f1=open("stamps.txt","r+")
input=f1.read()
print(input)
input=input.replace(',','\n')
input=input.replace('FROM F','AP')
input=input.replace('TO F','PA')
input=input.replace('TIMES','')
input=input.replace("'","")
input=input.replace("[","")
input=input.replace("]","")
print(input)
f2=open("stampsfromatted.txt","w+")
f2.write(input)
f1.close()
f2.close()

        
        
        