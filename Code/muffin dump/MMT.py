from fractions import gcd

from bounds import *

def relprime(a,b):
    return gcd(a,b) == 1

def g(s):
    m = (s**3 + 2*s**2 + s)/2
    while not(relprime(m,s)):
        m += 1
    print "s = "+str(s) + " m_0 = "+str(m)
    gs = -1
    while m>s:
        b = upper_bound(m,s)
        if b['bound_type'] == "Interval-Theorem":
            gs = m
            break
        m -= 1

    print "G("+str(s)+") = "+str(gs)

for s in range(31,100):
    g(s)
