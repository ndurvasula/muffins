from fractions import *
from math import *
from pprint import *
def f(s,mi,ms,O):
    f = open(O, 'w')
    out = ""
    for m in range(mi,ms+1):
        res = fc(m, s)
        if str(res) == str(None):
            res = "None\n"
        out += "m = "+str(m)+", s = "+str(s)+"\n"+str(res)+"\n"
    f.write(out)
    f.close()

#Currently assuming m, s are natural numbers
def fc(m, s):
    msg = ""
    #Easy cases (Theorem 0.1)
    if m%s == 0:
        return "Easy case: 1\n"
    if s%(2*m) == 0 and int(m/s) != m/s:
        return "Easy case: 1/2\n"
    if m == 1 or s%2 == 1 and m == 2:
        return "Easy case: 1/"+str(s)+"\n"

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
                axyz = [[xy[i][0][0],xy[i][0][1],z1],\
                        [xy[i][1][0],xy[i][1][1],z2]]
                r1 = axyz[0][1]*f+Fraction(axyz[0][2],2)
                r2 = axyz[1][1]*(1-f)+Fraction(axyz[1][2],2)
                r3 = axyz[1][1]*f+Fraction(axyz[1][2],2)
                r4 = axyz[0][1]*(1-f)+Fraction(axyz[0][2],2)
                if r1 == r2 and r1 == Fraction(m,s):
                    #We found a valid xyz set
                    xyz.append(axyz)
                elif r3 == r4 and r3 == Fraction(m,s):
                    #We found a valid set but x1 is actually x2
                    #and x2 is actually x1, so we swap them
                    temp = [axyz[0],axyz[1]]
                    axyz[0] = axyz[1]
                    axyz[1] = temp[0]
                    xyz.append(axyz)
            z1 += 1
    xyz.sort(key=lambda x: x[0][2]+x[1][2])
    xyz.reverse()

    if len(xyz) > 0:
        st = ""
        for i in range(len(xyz)):
            st+= "x1: "+str(xyz[i][0][0])+\
                ", x2: "+str(xyz[i][1][0])+\
                ", y1: "+str(xyz[i][0][1])+\
                ", y2: "+str(xyz[i][1][1])+\
                ", z1: "+str(xyz[i][0][2])+\
                ", z2: "+str(xyz[i][1][2])+"\n"
        if f >= 1/3:
            return "Floor ceiling + delta1: f("+str(m)+", "+str(s)+") = "+str(f.numerator)+"/"+str(f.denominator)+"\n"+st
        else:
            return "Delta1: f("+str(m)+", "+str(s)+") >= "+str(f.numerator)+"/"+str(f.denominator)+"\n"+st\
                   +"Floor ceiling method INCONCLUSIVE\n"

    else:
        msg += "No x y z pairs could be found for the delta 1 method\n"

    #Theorem 2.11 (delta 2)
    #All possible delta 2 values
    d2l = [Fraction(x,f.denominator) for x in range(f.numerator+1,ceil(f.denominator/2))]
    for d2 in d2l:
        #Find all possible x values
        x = []
        for x1 in range(s+1):
            for x2 in range(s+1):
                for x3 in range(s+1):
                    for x4 in range(s+1):
                        if x1+x2+x3+x4 == s:
                            x.append([x1,x2,x3,x4])

        #Find all possible values for equations 5-8
        eqs = []
        opt = [[f, d2],[f, 1-d2],[1-f, d2],[1-f, 1-d2]]
        for eq in opt:
            eqt = []
            for yd1 in range(int(m/(s*eq[0]))+1):
                for yd2 in range(int(m/(s*eq[1]))+1):
                    for z in range(int(2*m/s)+1):
                        if yd1*eq[0]+yd2*eq[1]+Fraction(z,2)==Fraction(m,s):
                            eqt.append([yd1,yd2,z])
            eqs.append(eqt)

        #Find what x values match to the y and z values
        #by seeing if they satisfy equations 1-3
        xyz = []
        for i in range(len(x)):
            x1 = x[i][0]
            x2 = x[i][1]
            x3 = x[i][2]
            x4 = x[i][3]
            for yz1 in eqs[0]:
                for yz2 in eqs[1]:
                    for yz3 in eqs[2]:
                        for yz4 in eqs[3]:
                            y11 = yz1[0]
                            y12 = yz1[1]
                            z1 = yz1[2]
                            
                            y21 = yz2[0]
                            y22 = yz2[1]
                            z2 = yz2[2]
                            
                            y31 = yz3[0]
                            y32 = yz3[1]
                            z3 = yz3[2]
                            
                            y41 = yz4[0]
                            y42 = yz4[1]
                            z4 = yz4[2]

                            #Check equations 1-3
                            if x1*y11 + x2*y21 == x3*y31 + x4*y41 and \
                               x1*y12 + x3*y32 == x2*y22 + x4*y42 and \
                               2*(m - (x1*y11 + x2*y21 + x1*y12 + x3*y32)) == z1*x1 + z2*x2 + z3*x3 + z4*x4:
                                xyz.append([d2,[x1,y11,y12,z1],[x2,y21,y22,z2],[x3,y31,y32,z3],[x4,y41,y42,z4]])

        xyz.sort(key=lambda x: (x[1][3]+x[2][3]+x[3][3]+x[4][3],x[1][3],x[2][3],x[3][3],x[4][3]))
        xyz.reverse()
        #Check if there are any valid xyz pairs
        if len(xyz) > 0:
            st = ""
            for i in range(len(xyz)):
                st+= "d2: "+str(xyz[i][0])+\
                    ", x1: "+str(xyz[i][1][0])+\
                    ", x2: "+str(xyz[i][2][0])+\
                    ", x3: "+str(xyz[i][3][0])+\
                    ", x4: "+str(xyz[i][4][0])+\
                    ", y11: "+str(xyz[i][1][1])+\
                    ", y12: "+str(xyz[i][1][2])+\
                    ", y21: "+str(xyz[i][2][1])+\
                    ", y22: "+str(xyz[i][2][2])+\
                    ", y31: "+str(xyz[i][3][1])+\
                    ", y32: "+str(xyz[i][3][2])+\
                    ", y41: "+str(xyz[i][4][1])+\
                    ", y42: "+str(xyz[i][4][2])+\
                    ", z1: "+str(xyz[i][1][3])+\
                    ", z2: "+str(xyz[i][2][3])+\
                    ", z3: "+str(xyz[i][3][3])+\
                    ", z4: "+str(xyz[i][4][3])+"\n"
            if f >= 1/3:
                return msg+"Floor ceiling + delta2: f("+str(m)+", "+str(s)+") = "+str(f.numerator)+"/"+str(f.denominator)+"\n"+st
            else:
                msg += "Delta2: f("+str(m)+", "+str(s)+") >= "+str(f.numerator)+"/"+str(f.denominator)+"\n"+st\
                   +"Floor ceiling method INCONCLUSIVE\n"
                return msg
        else:
            msg += "No x y z pairs could be found for the delta 2 method where delta2 = "+str(d2)+"\n"
            return msg
        
            
        
def factor(n):
    #returns a list of tuples containing factor pairs
    #e.g. factor(6) returns [(1, 6), (2, 3), (3, 2), (6, 1)]
    res = [(1,n),(n,1)]
    for i in range(2,n):
        for j in range(2,n):
            if i*j == n:
                res.append((i,j))
    return res
        
    
    
