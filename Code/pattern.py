from muffins import *

#Find a sequence in a pattern of Trues, Falses
def findPattern(seq):
	best = 2
	bestNum = 0
	bestWorks = []
	listOf = []
	#Try every mod pattern from 2...len(seq)^.5
	for mod in range(2,int((len(seq)+1)**.5)+2):
		print(mod)
		#Get the base values
		bases = []
		for i in range(0,mod):
			bases.append(seq[i])
		works = [True]*mod
		listOf = works	
		errors = 0
		attempts = 0
		for i in range(mod,len(seq)):
			attempts+=1
			if(seq[i] != bases[i%mod]):
				works[i%mod] = False
				listOf.append(False)
			else:
				listOf.append(True)
		if(works.count(True)/attempts>bestNum):
			bestNum = works.count(True)/attempts
			best = mod
			bestWorks = works	

	j = []
	
	for i in range(0,len(bestWorks)):
		if(bestWorks[i] == True):
			j.append(i)
	a = [best,bestNum]
	a.append(j)
	return [listOf,a]

def muffinsWork(students,muffinStart,muffinEnd,num):
	j = []
	for i in range(muffinStart,muffinEnd):
		j.append("No x y z pairs could be found for the delta "+str(num) not in fc(i,students))
	return j#findPattern(j)

studentNumber = int(input("How many students? "))
startValue = int(input("Muffin start? "))
endValue = int(input("Muffin end? "))

modNumber = int(input("What mod number? "))

for i in range(1,3):
	print("Currently working for delta "+str(i))
	results = muffinsWork(studentNumber,startValue,endValue,i)	
	'''
	partZero = results[0]
	partOne = results[1]

	num = 0 
	for i in range(0,len(partZero)):
		print(partZero[i],end="\t")
		num+=1
		if(num%partOne[0] == 0):
			print()
	'''

	num = 0
	for i in range(0,len(results)):
		if(results[i]):
			results[i] = 'T'
		else:
			results[i] = 'F'
		print(results[i],end=" ")
		if((i+1)%modNumber == 0 ):
			print()

	print()
