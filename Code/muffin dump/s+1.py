from bounds import *
print upper_bound(3,2)
print upper_bound(4,3)
print upper_bound(5,4)
for s in range(5,30):
    m = s+1
    a = upper_bound(s+1,s)["upper_bound"]
    if a == max(Fraction(1,3), min([Fraction(m,s*int(ceil(2.0*float(m)/float(s)))),1-Fraction(m,s*int(floor(2.0*float(m)/float(s))))])):
        print "1"
    elif a == Fraction(1,3):
        print "2"
    elif a > max(Fraction(1,3), min([Fraction(m,s*int(ceil(2.0*float(m)/float(s)))),1-Fraction(m,s*int(floor(2.0*float(m)/float(s))))])):
        print "3"
    else:
        print "4" 
