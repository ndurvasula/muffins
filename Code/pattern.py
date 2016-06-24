from muffins import *

#Find a sequence in a pattern of Trues, Falses
def findPattern(seq):
	best = 2
	bestNum = 0
	bestWorks = []
	#Try every mod pattern from 2...len(seq)^.5
	for mod in range(2,int((len(seq)+1)**.5)+1):
		#Get the base values
		bases = []
		for i in range(0,mod):
			bases.append(seq[i])
		works = [True]*mod	
		errors = 0
		attempts = 0
		for i in range(mod,len(seq)):
			attempts+=1
			if(seq[i] != bases[i%mod]):
				works[i%mod] = False
		if(works.count(True)/mod>bestNum):
			print(seq)
			bestNum = works.count(True)/mod
			best = mod
			bestWorks = works
	
	j = []
	
	for i in range(0,len(bestWorks)):
		if(bestWorks[i] == True):
			j.append(i)
	a = [best,bestNum]
	a.append(j)
	return a

def muffinsWork(students,muffinStart,muffinEnd):
	j = []
	for i in range(muffinStart,muffinEnd+1):
		j.append(calcMin(i,students) != None)
	return findPattern(j)

print(muffinsWork(5,1,50))	

