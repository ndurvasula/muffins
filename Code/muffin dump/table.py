from bounds import *
import pickle

"""G = pickle.load(open("G.txt","rb"))
for s in range(54,55):
    t = 0
    ot = []
    for i in range(1,2*s):
        if upper_bound(i,s)["upper_bound"] == Fraction(1,3):
            ot.append(i)
            t += 1
    mi = (s**3 + 2*s**2 + s)/2
    while gcd(mi,s)!=1:
        mi += 1
    intt = 0
    for i in range(1, G[s-7]):
        if upper_bound(i,s)["bound_type"] == "Interval-Theorem":
            intt += 1
    print str(s)+"&"+str(t)+"&"+str(intt)+"&"+str(G[s-7])+"&"+str(mi)+"\\\\ \hline"
"""
Ts = []
for s in range(7,55):
    for i in range(2*s,s,-1):
        if upper_bound(i,s)["upper_bound"] == Fraction(1,3):
            Ts.append(i)
            break
print Ts
