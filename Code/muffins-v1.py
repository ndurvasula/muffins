from fractions import *
from math import *
from pprint import *
def f(s,mi,ms,O):
    f = open(O, 'w')
    out = ""
    for m in range(mi,ms+1):
        out += "m = "+str(m)+"\ns = "+str(s)+"\n"+str(fc(m, s))+"\n\n"
    f.write(out)
    f.close()

#Currently assuming m, s are natural numbers
def fc(m, s):
    #Easy cases (Theorem 0.1)
    if m%s == 0:
        return "Easy case:\n1"
    if s%(2*m) == 0 and int(m/s) != m/s:
        return "Easy case:\n1/2"
    if m == 1 or s%2 == 1 and m == 2:
        return "Easy case:\n1/"+s

    #Not an easy case - try floor ceiling method
    #Assume f(m,s) > 1/3
    f = min([Fraction(m,s*ceil(2*m/s)),1-Fraction(m,s*floor(2*m/s))])
    
    #Check matching
    #Find x1,y1,x2,y2,z1,z2
    xy = []
    xyz = []
    
    #factors is a list that contains all xy pairs whose products are <=m
    factors = []
    for i in range(1,m+1):
        factors.append(factor(i))

    #Loop through each value in factors to find potential x1 and x2
    for i in range(len(factors)):
        for j in range(len(factors[i])):
            for k in range(j,len(factors[i])):
                if factors[i][j][0]+factors[i][k][0] == s:
                    xy.append([factors[i][j],factors[i][k]])

    #Find corresponding z values to x and y
    for i in range(len(xy)):
        #z1x1 + z2x2 = target
        target = 2*(m-xy[i][0][0]*xy[i][0][1])
        z1 = 0
        while z1*xy[i][0][0] <= target:
            z2 = (target-z1*xy[i][0][0])/xy[i][1][0]
            if z2 == int(z2):
                z2 = int(z2)
                axyz = [[xy[i][0][0],xy[i][0][1],z1],[xy[i][1][0],xy[i][1][1],z2]]
                r1 = axyz[0][1]*f+Fraction(axyz[0][2],2)
                r2 = axyz[1][1]*(1-f)+Fraction(axyz[1][2],2)
                r3 = axyz[1][1]*f+Fraction(axyz[1][2],2)
                r4 = axyz[0][1]*(1-f)+Fraction(axyz[0][2],2)
                if r1 == r2 and r1 == Fraction(m,s):
                    xyz.append(axyz)
                elif r3 == r4 and r3 == Fraction(m,s):
                    temp = [axyz[0],axyz[1]]
                    axyz[0] = axyz[1]
                    axyz[1] = temp[0]
                    xyz.append(axyz)
            z1 += 1
    xyz.sort(key=lambda x: x[0][2]+x[1][2])
    xyz.reverse()

    if len(xyz) > 0:
        return "Floor ceiling + delta1\n"+pformat(xyz)+"\n"+str(f.numerator)+"/"+str(f.denominator)
    

def factor(n):
    #returns a list of tuples containing factor pairs
    #e.g. factor(6) returns [(1,6), (2, 3)]
    res = [(1,n)]
    for i in range(2,n):
        for j in range(2,n):
            if i*j == n:
                res.append((i,j))
    return res
        
    
    
