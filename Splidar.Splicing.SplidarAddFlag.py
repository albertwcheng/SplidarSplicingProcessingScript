#!/usr/bin/env python

#
#
# version 2010-3-15
#

from sys import stderr, stdout,exit,argv
from albertcommon import *

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

def properpvalue(pvalues):
	n=0
	for p in pvalues:
		if p>=0 and p<=1:
			n+=1
	
	return n		

def pvalues2FDRInPlace(pvalues):
	pvalues.sort()
	totalNum=len(pvalues)
	properTotal=properpvalue(pvalues)
	pvi=0
	ppv=-100
	pvalues2FDRMap=dict()

	while pvi<totalNum:
		while ppv==pvalues[pvi]:
			pvi+=1
			if pvi==totalNum:
				break
			
		#now pvi is the number of pvalues<= previous pvalue
		
		if pvi>=1:
			if ppv>=0 and ppv<=1:
				FDR=float(properTotal)*ppv/pvi
				
			else:
				FDR=2	

			pvalues2FDRMap[ppv]=FDR	
		
		if pvi==totalNum:
			break		
		ppv=pvalues[pvi]

	return pvalues2FDRMap

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

def pvalue2FDRVector(pvv):
	pvalues=pvv[:]
	pvalue2FDRMap=pvalues2FDRInPlace(pvalues)
	
	FDRVector=[]
	for pvalue in pvv:
		FDRVector.append(pvalue2FDRMap[pvalue])

	return FDRVector

def transposeMatrix(matrix):
	nRows=len(matrix)
	if nRows<1:
		return []
	
	nCols=len(matrix[0]) #ASSUME COL SIZE
		

	TMatrix=[]	

	for c in range(0,nCols):
		newRow=[]
		for r in range(0,nRows):
			newRow.append(matrix[r][c])
		TMatrix.append(newRow)

	return TMatrix
	
	
	

		

def pvalue2FDRMatrix(matrix):
	FDRMatrix=[]

	pvalues=[]
	for pvalueRow in matrix:
		pvalues.extend(pvalueRow)

	pvalue2FDRMap=pvalues2FDRInPlace(pvalues)
	
	for row in matrix:
		newFDRRow=[]
		for pvalue in row:
			newFDRRow.append(pvalue2FDRMap[pvalue])

		FDRMatrix.append(newFDRRow)

	return FDRMatrix


#if len(sys.argv)!=4:
#	print >> stderr,sys.argv[0],"filename totalFlowThreshold JRThreshold"
#	sys.exit()

#now the real deal

startRow=2
headerRow=startRow-1
fs="\t"

try:
	print >> stderr,argv[0],"received arguments:",argv[1:]
	fileName,ThresholdIncExcReadsPerSample,ThresholdSumIncExcReadsSamplePair,incDetectionThreshold,excDetectionThreshold,JRThreshold=sys.argv[1:]
except:
	print >> stderr,argv[0],"fileName,ThresholdIncExcReadsPerSample,ThresholdSumIncExcReadsSamplePair,incDetectionThreshold,excDetectionThreshold,JRThreshold"
	exit()

header,prestarts=getHeader(fileName,headerRow,startRow,fs)

ThresholdIncExcReadsPerSample=int(ThresholdIncExcReadsPerSample)
ThresholdSumIncExcReadsSamplePair=int(ThresholdSumIncExcReadsSamplePair)
incDetectionThreshold=int(incDetectionThreshold)
excDetectionThreshold=int(excDetectionThreshold)
JRThreshold=int(JRThreshold)


eventLines=[]
totalFlowPvalueMatrix=[]
totalFlowDetectable=[]
totalFlowDetected=[]
totalFlowDetectedBoth=[]
JRFlagPvalueMatrix=[]
JRFlagDetectable=[]
JRFlagDetected=[]
JRFlagDetectedBoth=[]

		
IncPosCol=getCol0ListFromCol1ListStringAdv(header,".IncPos")[0]
ExcPosCol=getCol0ListFromCol1ListStringAdv(header,".ExcPos")[0]
IncExcReadCols=getCol0ListFromCol1ListStringAdv(header,"@Inc\\+ExcReads")
IncReadCols=getCol0ListFromCol1ListStringAdv(header,"@\\.IncReads")
ExcReadCols=getCol0ListFromCol1ListStringAdv(header,"@\\.ExcReads")

inJPFlagCol=getCol0ListFromCol1ListStringAdv(header,".inJPFlag")[0]
exJPFlagCol=getCol0ListFromCol1ListStringAdv(header,".exJPFlag")[0]

inJRFlagCols=getCol0ListFromCol1ListStringAdv(header,"@inJRFlag")
exJRFlagCols=getCol0ListFromCol1ListStringAdv(header,"@exJRFlag")
inJRCols=getCol0ListFromCol1ListStringAdv(header,"@inJR$")
exJRCols=getCol0ListFromCol1ListStringAdv(header,"@exJR$")

pvalueCols=getCol0ListFromCol1ListStringAdv(header,"@fisherpvalue")

print >> stderr,"IncPosCol",getVectorByIndexVector(header,[IncPosCol])
print >> stderr,"ExcPosCol",getVectorByIndexVector(header,[ExcPosCol])
print >> stderr,"IncExcReadCols",getVectorByIndexVector(header,IncExcReadCols)
print >> stderr,"IncReadCols",getVectorByIndexVector(header,IncReadCols)
print >> stderr,"ExcReadCols",getVectorByIndexVector(header,ExcReadCols)
print >> stderr,"inJPFlagCol",getVectorByIndexVector(header,[inJPFlagCol])
print >> stderr,"exJPFlagCol",getVectorByIndexVector(header,[exJPFlagCol])
print >> stderr,"inJRFlagCols",getVectorByIndexVector(header,inJRFlagCols)
print >> stderr,"exJRFlagCols",getVectorByIndexVector(header,exJRFlagCols)
print >> stderr,"inJRCols",getVectorByIndexVector(header,inJRCols)
print >> stderr,"exJRCols",getVectorByIndexVector(header,exJRCols)

samples=[]
for c in IncExcReadCols:
	samples.append(".".join(header[c].split(".")[0:-1]))

sampleComparisons=[]


nSamples=len(samples)



for i in range(0,nSamples-1):
	for j in range(i+1,nSamples):
		sampleComparisons.append(samples[j]+"-"+samples[i])

print >> stderr,"samples are",samples
print >> stderr,"sample comparisons are",sampleComparisons


fin=open(fileName)
lino=0
for line in fin:
	lino+=1
	line=line.rstrip("\r\n")
	fields=line.split(fs)	

 	if lino<startRow:
		print >> stdout, line+fs+"TFDetectable"+fs+fs.join(paste(sampleComparisons,".TFDetected"))+fs+"TFDetectedMax"+fs+fs.join(paste(sampleComparisons,".TFDetectedBoth"))+fs+"TFDetectedBothMax"+fs+"JFDetectable"+fs+fs.join(paste(sampleComparisons,".JFDetected"))+fs+"JFDetectedMax"+fs+fs.join(paste(sampleComparisons,".JFDetectedBoth"))+fs+"JFDetectedBothMax"+fs+fs.join(paste(sampleComparisons,".TFPvalue"))+fs+"TFPvalueMin"+fs+"TFPvalueMax"+fs+fs.join(paste(sampleComparisons,".JFPvalue"))+fs+"JFPvalueMin"+fs+"JFPvalueMax"+fs+fs.join(paste(sampleComparisons,".TFFDR"))+fs+"TFFDRMin"+fs+"TFFDRMax"+fs+fs.join(paste(sampleComparisons,".JFFDR"))+fs+"JFFDRMin"+fs+"JFFDRMax"
		continue
	
	eventLines.append(line)

	#total flow detectable
	if(int(fields[IncPosCol])>=1 and int(fields[ExcPosCol])>=1):
		ThisTotalFlowDetectable=True
	else:
		ThisTotalFlowDetectable=False
	
	totalFlowDetectable.append(BoolToInt(ThisTotalFlowDetectable))
	
	tmpRow=[]
	#total flow detected
	for i in range(0,nSamples-1):
		for j in range(i+1,nSamples):
			if not ThisTotalFlowDetectable:
				tmpRow.append(BoolToInt(False))
			else:
				incexci=int(fields[IncExcReadCols[i]])
				incexcj=int(fields[IncExcReadCols[j]])

				if incexci>=ThresholdIncExcReadsPerSample and incexcj>=ThresholdIncExcReadsPerSample and incexci+incexcj>=ThresholdSumIncExcReadsSamplePair:
					tmpRow.append(BoolToInt(True))
				else:
					tmpRow.append(BoolToInt(False))

	#tmpRow.append(max(tmpRow))
	totalFlowDetected.append(tmpRow)
	
	tmpRow=[]
	#total flow detected both
	for i in range(0,nSamples-1):
		for j in range(i+1,nSamples):
			if not ThisTotalFlowDetectable:
				tmpRow.append(BoolToInt(False))
			else:
				incexci=int(fields[IncExcReadCols[i]])
				incexcj=int(fields[IncExcReadCols[j]])
				inci=int(fields[IncReadCols[i]])
				exci=int(fields[ExcReadCols[i]])
				incj=int(fields[IncReadCols[j]])
				excj=int(fields[ExcReadCols[j]])


				if incexci>=ThresholdIncExcReadsPerSample and incexcj>=ThresholdIncExcReadsPerSample and incexci+incexcj>=ThresholdSumIncExcReadsSamplePair and max([inci,incj])>=incDetectionThreshold and max([exci,excj])>=excDetectionThreshold :
					tmpRow.append(BoolToInt(True))
				else:
					tmpRow.append(BoolToInt(False))

		

	#tmpRow.append(max(tmpRow))
	
	ThisTotalFlowDetectedBoth=tmpRow	
	totalFlowDetectedBoth.append(ThisTotalFlowDetectedBoth)

	

	pvalueV=getVectorByIndexVector(fields,pvalueCols)
	StringVectorToFloatVectorInPlace(pvalueV)

	tmpRow=[]
	
	nPvalueV=len(pvalueV)

	#print >> stderr,"pvalueV",pvalueV
	#print >> stderr,"thistotalFlowdetectedboth",ThisTotalFlowDetectedBoth

	for i in range(0,nPvalueV):
		if IntToBool(ThisTotalFlowDetectedBoth[i]):
			tmpRow.append(pvalueV[i])
		else:
			tmpRow.append(2)	
		
	totalFlowPvalueMatrix.append(tmpRow)

	##############
	##############
	##############


	#JRFlag detectable
	if(int(fields[inJPFlagCol])>=1 and int(fields[exJPFlagCol])>=1):
		ThisJRFlagDetectable=True
	else:
		ThisJRFlagDetectable=False
	
	JRFlagDetectable.append(BoolToInt(ThisJRFlagDetectable))
	

	tmpRow=[]
	#JRFlag Detected
	for i in range(0,nSamples-1):
		for j in range(i+1,nSamples):
			if not ThisJRFlagDetectable:
				tmpRow.append(BoolToInt(False))
			else:
				inexJRFlag1=int(fields[inJRFlagCols[i]])+int(fields[exJRFlagCols[i]])
				inexJRFlag2=int(fields[inJRFlagCols[j]])+int(fields[exJRFlagCols[j]])

				inJR1=int(fields[inJRCols[i]])
				inJR2=int(fields[inJRCols[j]])
				exJR1=int(fields[exJRCols[i]])
				exJR2=int(fields[exJRCols[j]])

				#inexJR1=inJR1+exJR1
				#inexJR2=inJR2+exJR2

				if(inexJRFlag1>0 and inexJRFlag2>0 and max([inJR1,exJR1])>JRThreshold and max([inJR2,exJR2])>JRThreshold ):
					tmpRow.append(BoolToInt(True))
				else:
					tmpRow.append(BoolToInt(False))

	#tmpRow.append(max(tmpRow))
	JRFlagDetected.append(tmpRow)
	
	tmpRow=[]
	#total flow detected both
	for i in range(0,nSamples-1):
		for j in range(i+1,nSamples):
			if not ThisJRFlagDetectable:
				tmpRow.append(BoolToInt(False))
			else:
				inexJRFlag1=int(fields[inJRFlagCols[i]])+int(fields[exJRFlagCols[i]])
				inexJRFlag2=int(fields[inJRFlagCols[j]])+int(fields[exJRFlagCols[j]])

				inJR1=int(fields[inJRCols[i]])
				inJR2=int(fields[inJRCols[j]])
				exJR1=int(fields[exJRCols[i]])
				exJR2=int(fields[exJRCols[j]])
				
				if(inexJRFlag1>0 and inexJRFlag2>0 and max([inJR1,exJR1])>JRThreshold and max([inJR2,exJR2])>JRThreshold and max([int(fields[inJRFlagCols[i]]),int(fields[inJRFlagCols[j]])])>0 and  max([int(fields[exJRFlagCols[i]]),int(fields[exJRFlagCols[j]])])>0 and max([inJR1,inJR2])>JRThreshold and max([exJR1,exJR2])>JRThreshold ):
					tmpRow.append(BoolToInt(True))
				else:
					tmpRow.append(BoolToInt(False))

		

	#tmpRow.append(max(tmpRow))
	
	ThisJRFlagDetectedBoth=tmpRow	
	JRFlagDetectedBoth.append(ThisJRFlagDetectedBoth)


	tmpRow=[]
	
	nPvalueV=len(pvalueV)

	for i in range(0,nPvalueV):
		if IntToBool(ThisJRFlagDetectedBoth[i]):
			tmpRow.append(pvalueV[i])
		else:
			tmpRow.append(2)	
		
	JRFlagPvalueMatrix.append(tmpRow)	

#totalFlowACFDRMatrix=pvalue2FDRMatrix(totalFlowPvalueMatrix)
#JRFlagACFDRMatrix=pvalue2FDRMatrix(JRFlagPvalueMatrix)


totalFlowPvalueMatrixT=transposeMatrix(totalFlowPvalueMatrix)
JRFlagPvalueMatrixT=transposeMatrix(JRFlagPvalueMatrix)

for r in range(0,len(totalFlowPvalueMatrixT)):
	totalFlowPvalueMatrixT[r]=pvalue2FDRVector(totalFlowPvalueMatrixT[r])


for r in range(0,len(JRFlagPvalueMatrixT)):
	JRFlagPvalueMatrixT[r]=pvalue2FDRVector(JRFlagPvalueMatrixT[r])

totalFlowFDRMatrix=transposeMatrix(totalFlowPvalueMatrixT)
JRFlagFDRMatrix=transposeMatrix(JRFlagPvalueMatrixT)



##
#eventLines=[]
#totalFlowPvalueMatrix=[]
#totalFlowDetectable=[]
#totalFlowDetected=[]
#totalFlowDetectedBoth=[]
#JRFlagPvalueMatrix=[]
#JRFlagDetectable=[]
#JRFlagDetected=[]
#JRFlagDetectedBoth=[]
#

#now output!~
for line,TFPvalue,TFFDR,TFDetectable,TFDetected,TFDetectedBoth,JFPvalue,JFFDR,JFDetectable,JFDetected,JFDetectedBoth in zip(eventLines,totalFlowPvalueMatrix,totalFlowFDRMatrix,totalFlowDetectable,totalFlowDetected,totalFlowDetectedBoth,JRFlagPvalueMatrix,JRFlagFDRMatrix,JRFlagDetectable,JRFlagDetected,JRFlagDetectedBoth):
	TFPvalueMin=min(TFPvalue)
	TFPvalueMax=max(TFPvalue)
	TFFDRMin=min(TFFDR)
	TFFDRMax=max(TFFDR)	
	TFDetectedMax=max(TFDetected)
	TFDetectedBothMax=max(TFDetectedBoth)
	JFPvalueMin=min(JFPvalue)
	JFPvalueMax=max(JFPvalue)
	JFFDRMin=min(JFFDR)
	JFFDRMax=max(JFFDR)
	JFDetectedMax=max(JFDetected)
	JFDetectedBothMax=max(JFDetectedBoth)

	ToStringVectorInPlace(TFPvalue)
	ToStringVectorInPlace(TFFDR)
	
	ToStringVectorInPlace(TFDetected)
	ToStringVectorInPlace(TFDetectedBoth)
	ToStringVectorInPlace(JFPvalue)
	ToStringVectorInPlace(JFFDR)

	ToStringVectorInPlace(JFDetected)
	ToStringVectorInPlace(JFDetectedBoth)

	print >> stdout, line+fs+str(TFDetectable)+fs+fs.join(TFDetected)+fs+str(TFDetectedMax)+fs+fs.join(TFDetectedBoth)+fs+str(TFDetectedBothMax)+fs+str(JFDetectable)+fs+fs.join(JFDetected)+fs+str(JFDetectedMax)+fs+fs.join(JFDetectedBoth)+fs+str(JFDetectedBothMax)+fs+fs.join(TFPvalue)+fs+str(TFPvalueMin)+fs+str(TFPvalueMax)+fs+fs.join(JFPvalue)+fs+str(JFPvalueMin)+fs+str(JFPvalueMax)+fs+fs.join(TFFDR)+fs+str(TFFDRMin)+fs+str(TFFDRMax)+fs+fs.join(JFFDR)+fs+str(JFFDRMin)+fs+str(JFFDRMax)
	
	
		 
		
			


fin.close()


