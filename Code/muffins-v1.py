from fractions import *
from math import *
from pprint import *
from util import *

#Print out all the values of f(m,s) for a fixed s
#And varying m from muffinStart to muffinEnd
def f(students,muffinStart,muffinEnd,fileName):
    f = open(fileName, 'w')
    out = ""
    for muffin in range(muffinStart,muffinEnd+1):
        out += "m = "+str(muffin)+", s = "+str(students)+"\n"+str(calcMin(muffin, students))+"\n"
    f.write(out)
    f.close()

#Currently assuming m, s are natural numbers
#Calculate the maximum, min size of a muffin piece
def calcMin(muffins, students):
    #Easy cases (Theorem 0.1)

    #The muffins is a multiple of the number of students
    #So give each of them m/s, which is a whole number
    if muffins%students == 0:
        return "Easy case: 1\n"

    #s is a multiple of 2m, give each student 1/2
    if students%(2*muffins) == 0 and int(muffins/students) != muffins/students:
        return "Easy case: 1/2\n"
    
    #One muffin needs to be split into s pieces
    #Or an odd number of students and 2 muffins
    if muffins == 1 or students%2 == 1 and muffins == 2:
        return "Easy case: 1/"+str(students)+"\n"

    #Not an easy case - try floor ceiling method
    #Assume f(m,s) > 1/3
    upperBound = min([Fraction(muffins,students*ceil(2*muffins/students)),1-Fraction(muffins,students*floor(2*muffins/students))])
    
    #Check matching
    #Find x1,y1,x2,y2,z1,z2
    #Which is the number of people who get delta, and 1-delta sized pieces
    xy = []
    xyz = []
    
    #Factors is a list that contains all xy pairs whose products are <=m
    #AKA x1y1 = x2y2<=m
    factors = []
    for i in range(1,muffins+1):
        factors.append(factor(i))

    #Loop through each value in factors to find potential x1 and x2
    for i in range(len(factors)):
        for j in range(len(factors[i])):
            for k in range(j,len(factors[i])):
                if factors[i][j][0]+factors[i][k][0] == students:
                    xy.append([factors[i][j],factors[i][k]])

    #AKA how many people get (1/2) sized pieces
    #Find corresponding z values to x and y
    for i in range(len(xy)):
        #z1x1 + z2x2 = target
        target = 2*(muffins-xy[i][0][0]*xy[i][0][1])
        z1 = 0
        while z1*xy[i][0][0] <= target:
            z2 = (target-z1*xy[i][0][0])/xy[i][1][0]
            if z2 == int(z2):
                z2 = int(z2)
                axyz = [[xy[i][0][0],xy[i][0][1],z1],\
                        [xy[i][1][0],xy[i][1][1],z2]]
                r1 = axyz[0][1]*upperBound+Fraction(axyz[0][2],2)
                r2 = axyz[1][1]*(1-upperBound)+Fraction(axyz[1][2],2)
                r3 = axyz[1][1]*upperBound+Fraction(axyz[1][2],2)
                r4 = axyz[0][1]*(1-upperBound)+Fraction(axyz[0][2],2)
                if r1 == r2 and r1 == Fraction(muffins,students):
                    xyz.append(axyz)
                elif r3 == r4 and r3 == Fraction(muffins,students):
                    temp = [axyz[0],axyz[1]]
                    axyz[0] = axyz[1]
                    axyz[1] = temp[0]
                    xyz.append(axyz)
            z1 += 1
    xyz.sort(key=lambda x: x[0][2]+x[1][2])
    xyz.reverse()

    #If there is a triplet that matches
    if len(xyz) > 0:
        returnString = ""
        for i in range(len(xyz)):
            returnString += "x1: "+str(xyz[i][0][0])+\
                ", x2: "+str(xyz[i][1][0])+\
                ", y1: "+str(xyz[i][0][1])+\
                ", y2: "+str(xyz[i][1][1])+\
                ", z1: "+str(xyz[i][0][2])+\
                ", z2: "+str(xyz[i][1][2])+"\n"
        if upperBound >= 1/3:
            return "Floor ceiling + delta1: f("+str(muffins)+", "+str(students)+") = "+str(upperBound.numerator)+"/"+str(upperBound.denominator)+"\n"+returnString
        else:
            return "Delta1: f("+str(muffins)+"+, "+str(students)+") >= "+str(upperBound.numerator)+"/"+str(upperBound.denominator)+"\n"+returnString\
                   +"\nFloor ceiling method INCONCLUSIVE"
    
f(3,1,5,"output.txt")
