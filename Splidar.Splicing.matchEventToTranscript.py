#!/usr/bin/env python

from sys import *
from os import system,unlink
from tempfile import *

def getTempFileName():
	f=NamedTemporaryFile(delete=False)
	fileName=f.name
	f.close()
	return fileName
	
def deleteTempFile(fileName):
	unlink(fileName)


def matchEvent_bestBounds(ev1bounds,ev2bounds):
	#if len(ev1bounds)!=len(ev2bounds):
	#	return False
	
	if len(ev1bounds)==0 or len(ev2bounds)==0:
		print >> stderr,"Error! Either ev1bounds or ev2bounds has nothing in it"
		return False
	
	if len(ev1bounds)==1:
		#there's gonna be no intron for inner bounds,just found complete
		ev1start,ev1end=ev1bounds[0]
		for ev2start,ev2end in ev2bounds:
			if ev1start>=ev2start and ev1end<=ev2end:
				return True
				
			if ev2start>ev1end:
				return False
		
		return False
	else:
		ev1boundsExpanded=[]
		ev2boundsExpanded=[]
		
		for ev1bound in ev1bounds:
			ev1boundsExpanded.extend(ev1bound)
		
		for ev2bound in ev2bounds:
			ev2boundsExpanded.extend(ev2bound)
		
		lev2bound=len(ev2boundsExpanded)
		
		#find the first bound!
		try:
			starter2=ev2boundsExpanded.index(ev1boundsExpanded[1],1,lev2bound-1)
		except ValueError: #not even the first bound is found
			return False
		
		
		
		i2=starter2
		#then inner bounds should be the same
		for i in range(1,len(ev1boundsExpanded)-1):
			if i2>=lev2bound-1:
				return False #exhausted inner coordinates of ev2boundExpanded (of the transcript)
			if ev1boundsExpanded[i]!=ev2boundsExpanded[i2]:
				return False
			i2+=1
			
		return True







def chromStartBlockStartsSizes2GenomicCoordinates(chromStart,blockStarts,blockSizes):
	blocks=[]
	chromStart=int(chromStart)
	for blockStart,blockSize in zip(blockStarts,blockSizes):
		if len(blockStart)==0 or len(blockSize)==0:
			continue #empty 1,424,523,*
		blockStart=int(blockStart)
		blockSize=int(blockSize)
		newBlock=(chromStart+blockStart,chromStart+blockStart+blockSize)
		blocks.append(newBlock)
	return blocks



def printUsageAndExit(programName):
	print >> stderr,"Usage:",programName,"eventBed transcriptBed" # method["+",".join(methods.keys())+"]"
	exit()

if __name__=='__main__':
	programName=argv[0]
	args=argv[1:]
	try:
		ev1bed,ev2bed=args #,method=args
	except:
		printUsageAndExit(programName)




	
	func=matchEvent_bestBounds

	
		
	#first of all, join the bed files by overlap to simply computation
	
	tmpFileName=getTempFileName()
	
	
	###tmpFileName="/tmp/tmp5_bZgi"
	
	###print >> stderr,tmpFileName
	
	#tmpFileName="tmp.00"
	
	
	###system(" ".join(["joinBedByOverlap.py",ev1bed,ev2bed,">",tmpFileName]))
	
	#system(" ".join(["colStat.py",tmpFileName]))
	
	#now open the tmp file (the ebedebed)
	'''
[:::::			R 1			:::::]
Index			Excel			Field
-----			-----			-----
1			A			chr19
2			B			9391740
3			C			9405459
4			D			A5SS.ZNF266.9832.1
5			E			0
6			F			-
7			G			9391740
8			H			9405459
9			I			255,0,0
10			J			2
11			K			154,116
12			L			0,13603
13			M			chr19
14			N			9391666
15			O			9407216
16			P			ZNF266.jApr07
17			Q			0
18			R			-
19			S			9391668
20			T			9407175
21			U			0
22			V			3
23			W			228,86,257,
24			X			0,15117,15293,


	'''
	matchedEventons=dict() #matchedEventons[ev1eventID][ev2eventID]=    +1: first of pair matched +2 second of pair matched
	
	#print tmpFileName
	fil=open(tmpFileName)
	lino=0
	for lin in fil:
		lino+=1
		fields=lin.rstrip("\r\n").split()
		#print >> stderr,fields
		try:
			ev1bounds=chromStartBlockStartsSizes2GenomicCoordinates(fields[1],fields[11].split(","),fields[10].split(","))
			
		except:
			print >> stderr,"formating error for ev1bound",fields[1],fields[11],fields[10],"at line",lino
			exit()
		try:
			ev2bounds=chromStartBlockStartsSizes2GenomicCoordinates(fields[13],fields[23].split(","),fields[22].split(","))
		except:
			print >> stderr,"formating error for eve2bound",fields[13],fields[23],fields[22],"at line",lino
			exit()
			
		ev1ID=fields[3] #A5SS.ZNF266.9832.1
		ev2ID=fields[15] #ZNF266.jApr07
		ev1eventID=ev1ID
		ev2eventID=ev2ID
		#print >> stderr,"ev1bounds=",ev1bounds
		#print >> stderr,"ev2bounds=",ev2bounds
		#ev1pairID=int(ev1ID.split(".")[-1])  #1
		#ev2pairID=int(ev2ID.split(".")[-1])  #1
		matched=func(ev1bounds,ev2bounds)
		
		if matched:
			print >> stdout,ev1ID+"\t"+ev2ID
			
			#matchPairFlag=ev1pairID*10+ev2pairID #10+1=11
			#if ev1eventID not in matchedEventons:
			#	matchedEventons[ev1eventID]=dict()
			#if ev2eventID not in matchedEventons[ev1eventID]:
			#	matchedEventons[ev1eventID][ev2eventID]=[]
			#if matchPairFlag in matchedEventons[ev1eventID][ev2eventID]:
			#	print >> stderr,"error"
			#	exit()
			#matchedEventons[ev1eventID][ev2eventID].append(matchPairFlag)	
		
	fil.close()
	
	
	#now find all good matches
	#for ev1eventID,matchDict in matchedEventons.items():
	#	for ev2eventID,matchPairFlags in matchDict.items():
	#		matchPairFlags.sort()
	#		if len(matchPairFlags)==2 and ( ( 11 in matchPairFlags and 22 in matchPairFlags) or ( 12 in matchPairFlags and 21 in matchPairFlags) ):
	#			print >> stdout,"\t".join([ev1eventID,ev2eventID,str(matchPairFlags[0]),str(matchPairFlags[1])])
	
	
	
	
	deleteTempFile(tmpFileName)