#!/usr/bin/env python

import sys
from sys import stderr, stdout,exit,argv
from albertcommon import *
from getopt import getopt

def getVectorByIndexVector(datavector,indexvector):
	v=[]
	for idx in indexvector:
		v.append(datavector[idx])

	return v


def ToStringVectorInPlace(V):
	for i in range(0,len(V)):
		V[i]=str(V[i])

def StringVectorToIntVectorInPlace(V):
	for i in range(0,len(V)):
		V[i]=int(V[i])	

def StringVectorToFloatVectorInPlace(V):
	for i in range(0,len(V)):
		V[i]=float(V[i])	

def median(A):
	Ap=A[:]
	Ap.sort()
	return Ap[len(Ap)/2]

def addVectors(A,B):
	C=[]
	for a,b in zip(A,B):
		C.append(a+b)

	return C

def BoolToInt(b):
	if b:
		return 1
	else:
		return 0

def IntToBool(i):
	return i==1


def paste(v,s):
	newv=[]
	for vv in v:
		newv.append(vv+s)
	return newv

def printUsageAndExit(programName):
	print >> stderr, programName,"[options] fgset bgset bgpowersetprefix"
	print >> stderr, "[options]"
	print >> stderr,"\t","--mmIncExcReadsOff turn off min over events and samples [incExcReads] filter"
	print >> stderr,"\t","--mmNINE+Off turn off min over events and samples [NI+NE+] filter"
	print >> stderr,"\t","--mSIncExcReadsOff turn off min over events sum over samples [incExcReads] filter"
	print >> stderr,"\t","--mSNINE+Off turn off min over events sum over samples [NI+NE+] filter"
	print >> stderr,"\t","--startRow r[=2]"
	print >> stderr,"\t","--headerRow r[=startRow-1]"
	print >> stderr,"\t","--bg-subset-selector colselector[=no:use all rows|@TFDetectedBoth$]"
	print >> stderr,"\t","--incexcReads-selector colselector[=@Inc\\+ExcReads$]"
	print >> stderr,"\t","--NI-selector colselector[=@NI$]"
	print >> stderr,"\t","--NEp-selector colselector[=@NE\\+$]"
	print >> stderr,"\t","--iterate-median-B4 numMaxIter"

	exit() 

if __name__=='__main__':

	#get the arguments:
	mmIncExcReads=True
	mmNINEp=True
	mSIncExcReads=True
	mSNINEp=True
	bgSubsetSelector="@TFDetectedBoth$"
	incExcReadSelector="@Inc\\+ExcReads$"
	NISelector="@NI$"
	NEpSelector="@NE\\+$"

	startRow=2
	headerRow=-1
	iterateMedianB4=1

	fs="\t"

	programName=argv[0]
	try:
		opts,args=getopt(argv[1:],'',['mmIncExcReadsOff','mmNINE+Off','mSIncExcReadsOff','mSNINE+Off','startRow=','headerRow=','bg-subset-selector=','incexcReads-selector=','NI-selector=','NEp-selector=','iterate-median-B4='])

		for o,v in opts:
			if o=='--mmIncExcReadsOff':
				mmIncExcReads=False
			elif o=='--mmNINE+Off':
				mmNINEp=False
			elif o=='--mSIncExcReadsOff':
				mSIncExcReads=False
			elif o=='--mSNINE+Off':
				mSNINEp=False
			elif o=='--startRow':
				startRow=int(v)
			elif o=='--headerRow':
				headerRow=int(v)
			elif o=='--bg-subset-selector':
				bgSubsetSelector=v
			elif o=='--incexcReads-selector':
				incExcReadSelector=v
			elif o=='--NI-selector':
				NISelector=v
			elif o=='--NEp-selector':
				NEpSelector=v
			elif o=='--iterate-median-B4':
				iterateMedianB4=int(v)

		fgset,bgset,bgpowersetpref=args
	except:
		printUsageAndExit(programName)

	
	mmIncExcReadsThreshold=1000000000
	mSIncExcReadsThreshold=1000000000
	mmNINEpThreshold=1000000000
	mSNINEpThreshold=1000000000


	#now the real deal
	if headerRow==-1:
		headerRow=startRow-1


	
	#get columns for the different fields
	header,prestarts=getHeader(fgset,headerRow,startRow,fs)

	if mmIncExcReads or mSIncExcReads:
		IncExcReadCols=getCol0ListFromCol1ListStringAdv(header,incExcReadSelector)
		print >> stderr,"#IncExcReadCols",getVectorByIndexVector(header,IncExcReadCols)
	else:
		IncExcReadCols=[]

	
	if mmNINEp or mSNINEp:
		NICols=getCol0ListFromCol1ListStringAdv(header,NISelector)
		NEpCols=getCol0ListFromCol1ListStringAdv(header,NEpSelector)
		print >> stderr,"#NICols",getVectorByIndexVector(header,NICols)
		print >> stderr,"#NE+Cols",getVectorByIndexVector(header,NEpCols)
	else:
		NICols=[]
		NEpCols=[]
	
	
	if bgSubsetSelector.lower()=="no":
		subsetSelectorCols=[]
	else:
		subsetSelectorCols=getCol0ListFromCol1ListStringAdv(header,bgSubsetSelector)


	samples=[]
	for c in IncExcReadCols:
		samples.append(".".join(header[c].split(".")[0:-1]))

	sampleComparisons=[]


	nSamples=len(samples)



	for i in range(0,nSamples-1):
		for j in range(i+1,nSamples):
			sampleComparisons.append(samples[j]+"-"+samples[i])

	print >> stderr,"#samples are",samples
	print >> stderr,"#sample comparisons are",sampleComparisons


	B4Statistics=[]
	B3Statistics=[]
	B2Statistics=[]
	B1Statistics=[]	

	fin=open(fgset)
	lino=0
	for line in fin:
		lino+=1
		line=line.rstrip("\r\n")
		fields=line.split(fs)	

	 	if lino<startRow:
			#print >> stdout,line
			continue
		
		


		
		if len(IncExcReadCols)>0:
			IncExcReadVaules=getVectorByIndexVector(fields,IncExcReadCols)
			StringVectorToIntVectorInPlace(IncExcReadVaules)

		if len(NICols)>0:
			NIValues=getVectorByIndexVector(fields,NICols)
			StringVectorToIntVectorInPlace(NIValues)

		if len(NEpCols)>0:
			NEpValues=getVectorByIndexVector(fields,NEpCols)
			StringVectorToIntVectorInPlace(NEpValues)

		
		if len(NICols)>0 and len(NEpCols)>0:
			NINEpValues=addVectors(NIValues,NEpValues)


		if mmIncExcReads:
			if len(IncExcReadVaules)<1:
				print >> stderr,"#inc exc read columns not defined. Abort"
				exit()

			B1=min(IncExcReadVaules)
			mmIncExcReadsThreshold=min([mmIncExcReadsThreshold,B1])
			B1Statistics.append(B1)

		if mSIncExcReads:
			if len(IncExcReadVaules)<1:
				print >> stderr,"#inc exc read columns not defined. Abort"
				exit()		
			B2=sum(IncExcReadVaules)	
			mSIncExcReadsThreshold=min([mSIncExcReadsThreshold,B2])
			B2Statistics.append(B2)

		if mmNINEp:
			if len(NINEpValues)<1:
				print >> stderr,"#NI NE+ columns not defined. Abort"
				exit()
			#print >> stderr,"where NI=",NIValues,"NE+=",NEpValues,"NINE+",NINEpValues,"incexcreads",IncExcReadVaules,sum(IncExcReadVaules)
			B3=min(NINEpValues)
			mmNINEpThreshold=min([mmNINEpThreshold,B3])
			B3Statistics.append(B3)

		if mSNINEp:
			if len(NINEpValues)<1:
				print >> stderr,"#NI NE+ columns not defined. Abort"
				exit()
			B4=sum(NINEpValues)
			mSNINEpThreshold=min([mSNINEpThreshold,B4])
			B4Statistics.append(B4)

		

	fin.close()
	
	fgMedianB4=median(B4Statistics)
	fgMedianB3=median(B3Statistics)
	fgMedianB2=median(B2Statistics)
	fgMedianB1=median(B1Statistics)
	
	print >> stderr,"#fgMedianB4=",fgMedianB4

	bgMedianB4=-1

	trialn=0

	while bgMedianB4<fgMedianB4 and iterateMedianB4>=1:
		trialn+=1

		linesToOutput=[]
		B4Statistics=[]
		B3Statistics=[]
		B2Statistics=[]
		B1Statistics=[]		
	

		if mmIncExcReads:
			print >> stderr,"#using min min incexcread threshold",mmIncExcReadsThreshold

		if mSIncExcReads:
			print >> stderr,"#using min sum incexcread threshold",mSIncExcReadsThreshold

		if mmNINEp:
			print >> stderr,"#using min min NI NE+ threshold",mmNINEpThreshold

		if mSNINEp:
			print >> stderr,"#using min sum NI NE+ threshold",mSNINEpThreshold

		if len(subsetSelectorCols)>0:
			print >> stderr,"#using bg subset selector cols",subsetSelectorCols,getVectorByIndexVector(header,subsetSelectorCols)


	

		fin=open(bgset)
		lino=0
		for lin in fin:
			lino+=1
			#lin=lin.rstrip()
			fields=lin.rstrip().split(fs)
			if lino<startRow:
				linesToOutput.append(lin) #+"\n"
				continue

			if len(subsetSelectorCols)>0:
				for subsetSelector in subsetSelectorCols:
					if int(fields[subsetSelector])<=0:
						continue		

			if len(IncExcReadCols)>0:
				IncExcReadVaules=getVectorByIndexVector(fields,IncExcReadCols)
				StringVectorToIntVectorInPlace(IncExcReadVaules)

			if len(NICols)>0:
				NIValues=getVectorByIndexVector(fields,NICols)
				StringVectorToIntVectorInPlace(NIValues)

			if len(NEpCols)>0:
				NEpValues=getVectorByIndexVector(fields,NEpCols)
				StringVectorToIntVectorInPlace(NEpValues)

		
			if len(NICols)>0 and len(NEpCols)>0:
				NINEpValues=addVectors(NIValues,NEpValues)





			if mmIncExcReads:
				if len(IncExcReadVaules)<1:
					print >> stderr,"#inc exc read columns not defined. Abort"
					exit()	

				if min(IncExcReadVaules)<mmIncExcReadsThreshold:
					continue

			if mSIncExcReads:
				if len(IncExcReadVaules)<1:
					print >> stderr,"#inc exc read columns not defined. Abort"
					exit()	

				if sum(IncExcReadVaules)<mSIncExcReadsThreshold:
					continue		

			if mmNINEp:
				if len(NINEpValues)<1:
					print >> stderr,"#NI NE+ columns not defined. Abort"
					exit()
				B3=min(NINEpValues)
				if B3<mmNINEpThreshold:
					continue


			if mSNINEp:
				if len(NINEpValues)<1:
					print >> stderr,"#NI NE+ columns not defined. Abort"
					exit()

				B4=sum(NINEpValues)
				

				if B4<mSNINEpThreshold:
					continue
			
		
			B1Statistics.append(B1)
			B2Statistics.append(B2)
			B3Statistics.append(B3)					
			B4Statistics.append(B4)	
					
			linesToOutput.append(lin) #+"\n"
			#print >> stdout,lin
		
		

		fin.close()
		
		bgMedianB4=median(B4Statistics)
		bgMedianB3=median(B3Statistics)
		bgMedianB2=median(B2Statistics)
		bgMedianB1=median(B1Statistics)


		powersetfilename=bgpowersetpref+"_fgm_"+str(fgMedianB4)+"_bgm_"+str(bgMedianB4)+".xls"
		fil=open(powersetfilename,"w")
		fil.writelines(linesToOutput)
		fil.close()
		

		print >> stderr,"#trial",trialn
		print >> stderr,"#foreground median B4=",fgMedianB4,"power set median B4=",bgMedianB4
		print >> stderr,"#foreground median B3=",fgMedianB3,"power set median B3=",bgMedianB3
		print >> stderr,"#foreground median B2=",fgMedianB2,"power set median B2=",bgMedianB2
		print >> stderr,"#foreground median B1=",fgMedianB1,"power set median B1=",bgMedianB1
		print >> stderr,"#",(len(linesToOutput)-startRow+1),"events outputed to this power set"
		
		if trialn==1: #same for any trials, output only during the first time
			print >> stderr,"fps_fgMedianB4="+str(fgMedianB4)
			print >> stderr,"fps_fgMedianB3="+str(fgMedianB3)
			print >> stderr,"fps_fgMedianB2="+str(fgMedianB2)
			print >> stderr,"fps_fgMedianB1="+str(fgMedianB1)
			print >> stderr,"fps_sigset="+fgset
			print >> stderr,"fps_bgset="+fgset
		

		print >> stderr,"fps_psetMedianB4["+str(trialn)+"]="+str(bgMedianB4)
		
		print >> stderr,"fps_psetMedianB3["+str(trialn)+"]="+str(bgMedianB3)
		
		print >> stderr,"fps_psetMedianB2["+str(trialn)+"]="+str(bgMedianB2)
		
		print >> stderr,"fps_psetMedianB1["+str(trialn)+"]="+str(bgMedianB1)

		print >> stderr,"fps_pset["+str(trialn)+"]="+powersetfilename

	
		#determine next set of bounds
		minThreshold=max([1,min([mmIncExcReadsThreshold,mSIncExcReadsThreshold,mmNINEpThreshold,mSNINEpThreshold])]) #to avoid crashes div by 0.
		mmIncExcReadsThreshold+=mmIncExcReadsThreshold/minThreshold
		mSIncExcReadsThreshold+=mSIncExcReadsThreshold/minThreshold
		mmNINEpThreshold+=mmNINEpThreshold/minThreshold
		mSNINEpThreshold+=mSNINEpThreshold/minThreshold

