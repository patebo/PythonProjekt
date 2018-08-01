# BasicPythonProjekt
Problem sets solved on Python

Problem 1: Write a programme that takes a mathematical expression as an input (using Input command) and returns the outcome. The mathematical expression can only contain 1-digit numbers, the addition operator '+' and multiplication operator '*' 
a = input()
c = []
i = 0
# put all the multiplication in the expression into a list
while i<(len(a)-1):
    if a[i] == "*":
        b = ""
        b = b+a[i-1]
        for j in range(i,len(a)):
            if a[j] != "+":
                b = b+a[j]
                i = j
            else: 
                break
        c.append(b)
        i = i+1
    else: i = i+1
# calculate all the addition 
s = 0
if a[1] == "+": s = s+int(a[0])
if a[len(a)-2] == "+": s = s+int(a[len(a)-1])
for i in range(2,len(a)-2):
    if (a[i-1] == '+' and a[i+1] == '+'):
        s = s+int(a[i])
for u in c:
    p = 1
    for v in range(0,len(u),2): # calculate all the multiplication in the list
        p = p*int(u[v])
    s = s+p   
print(s)    
