#!/usr/bin/env python
#

#
#  Version 2010-3-15
#

import sys;
from sys import stdout, stderr
from math import fabs;
from albertcommon import *

#filter first by [ both events supported by JR ] then by [cobound (optional)] then by (IE+[NE+] or pvalue)


def getVectorByIndexVector(datavector,indexvector):
	v=[]
	for idx in indexvector:
		v.append(datavector[idx])

	return v

def getCatId(spliton,cols):
	return "#".join(getVectorByIndexVector(spliton,cols))


def StringVectorToIntVectorInPlace(V):
	for i in range(0,len(V)):
		V[i]=int(V[i])	

def StringVectorToFloatVectorInPlace(V):
	for i in range(0,len(V)):
		V[i]=float(V[i])	

def filterSameEvent(filename,startRow1,idCols,inJRFCols,exJRFCols,incExcReadCols,NICols,NECols,pvalueCols,ThresholdBothJRFPooledSample,ThresholdEitherJRFPerSample,ThresholdSumIncExcReadsPooledSample ,ThresholdIncExcReadsPerSample,favorFlankingCobound,criteria):

	fin=open(filename);


	linesMem=dict();
	linesCriteria=dict();
	BothJRFPooledSample=dict(); 
	CountEitherJRFPerSample=dict();
	IncExcReadsPooledSample=dict()
	CountIncExcReadsPerSample=dict();
	CoBound=dict();

	lino=0;
	for lin in fin:
		lino+=1;
		lin=lin.strip();
		spliton=lin.split("\t");
		
		eventKey=getCatId(spliton,idCols)
		inJRFV=getVectorByIndexVector(spliton,inJRFCols)
		exJRFV=getVectorByIndexVector(spliton,exJRFCols)
		incExcReadValues=getVectorByIndexVector(spliton,incExcReadCols)
		NIV=getVectorByIndexVector(spliton,NICols)
		NEV=getVectorByIndexVector(spliton,NECols)
		pvalueV=getVectorByIndexVector(spliton,pvalueCols)
		

		if(lino<startRow1):
			print >> sys.stdout, lin;
			#print >> sys.stderr, eventKey+"\t"+("\t".join(inJRFV))+"\t"+("\t".join(exJRFV))+"\t"+("\t".join(NIV))+"\t"+("\t".join(NEV))+"\t"+("\t".join(pvalueV));
			continue;
		

		
		
		
		
		StringVectorToIntVectorInPlace(inJRFV)
		StringVectorToIntVectorInPlace(exJRFV)
		StringVectorToIntVectorInPlace(NIV)
		StringVectorToIntVectorInPlace(NEV)
		StringVectorToIntVectorInPlace(incExcReadValues)
		StringVectorToFloatVectorInPlace(pvalueV)

		#now requires max(inJRFV) >0 && max(exJRV) >0 && per inJRV+exJRV > 0
		
		#thisJRFlag=1


		thisBothJRFPooledSample=0
		thisCountEitherJRFPerSample=0
		thisIncExcReadPooledSample=0
		thisCountIncExcReadsPerSample=0
		


		if (sum(inJRFV)>=ThresholdBothJRFPooledSample) and (sum(exJRFV)>=ThresholdBothJRFPooledSample):
			
			thisBothJRFPooledSample=1 #both inclusion and exclusion junction reads are detected in the pooled sample

		

		for inJRF,exJRF in zip(inJRFV,exJRFV):
			if inJRF>=ThresholdEitherJRFPerSample or exJRF>=ThresholdEitherJRFPerSample:  #how many samples does the event detected in either or both inclusion and exclusion junctions
				thisCountEitherJRFPerSample+=1

		#for NI,NE in zip(NIV,NEV):
		#	if NI+NE>ThresholdNINEPerSample:
		#		thisCountNINEPerSample+=1
		if sum(incExcReadValues)>=ThresholdSumIncExcReadsPooledSample:
			thisIncExcReadPooledSample=1

		for incexc in incExcReadValues:
			if incexc>=ThresholdIncExcReadsPerSample:
				thisCountIncExcReadsPerSample+=1
		
				

		#if max(inJRFV)<=0 or max(exJRFV)<=0: ## was max(exJRFV)>0 ?!?!?
		#	thisJRFlag=0
		#else:
		#	for inJRF,exJRF in zip(inJRFV,exJRFV):
		#		if inJRF+exJRF<=0:
		#			thisJRFlag=0

		if favorFlankingCobound>=0:
			thisCoBound=int(spliton[favorFlankingCobound])
		else:
			thisCoBound=0

	
				
		
		
		if criteria=="t":
			thisNINETotal=sum(NIV)+sum(NEV)		
			thisCriteria=thisNINETotal;
		elif criteria=="mmp":
			thisCriteria=1-min(pvalueV) #minimize min(pvalue)
		elif criteria=="xmp":
			thisCriteria=min(pvalueV) #maximize min(pvalue)
		elif criteria=="mxp":
			thisCriteria=1-max(pvalueV) #minmize max(pvalue)
		elif criteria=="xxp":
			thisCriteria=max(pvalueV) #maximize max(pvalue)
		else:
			print >> sys.stderr,"Unknown Criteria",criteria,". Abort"
			sys.exit()
	
		
		eventIsBetter=False
		


		if(linesMem.has_key(eventKey)):
			#if(thisJRFlag>linesJRFFlag[eventKey] or (thisJRFlag==linesJRFFlag[eventKey] and thisCriteria>linesCriteria[eventKey])): #found a better line
			if thisBothJRFPooledSample==BothJRFPooledSample[eventKey]:
				
				if thisCountEitherJRFPerSample==CountEitherJRFPerSample[eventKey]: #use the cobound criteria
					
					if thisIncExcReadPooledSample==IncExcReadsPooledSample[eventKey]:
						
						if thisCountIncExcReadsPerSample==CountIncExcReadsPerSample[eventKey]:
						
							if thisCoBound==CoBound[eventKey]:
								eventIsBetter=(thisCriteria>linesCriteria[eventKey])
							else:
								eventIsBetter=(thisCoBound>CoBound[eventKey])
						else:
							eventIsBetter=(thisCountIncExcReadsPerSample>CountIncExcReadsPerSample[eventKey])
					else:
						eventIsBetter=(thisIncExcReadPooledSample>IncExcReadsPooledSample[eventKey])
				else:
					eventIsBetter=(thisCountEitherJRFPerSample>CountEitherJRFPerSample[eventKey])
			else:
				eventIsBetter=(thisBothJRFPooledSample>BothJRFPooledSample[eventKey])
		else:
			eventIsBetter=True
								
		if eventIsBetter:
			
			#if eventKey in linesMem:				
			#	print >> stderr,spliton[0],"is better by than",thisBothJRFPooledSample,BothJRFPooledSample[eventKey],linesMem[eventKey]
			#else:
			#	print >> stderr,"adding first",spliton[0],"for",eventKey,thisBothJRFPooledSample

			linesMem[eventKey]=lin;
			

			BothJRFPooledSample[eventKey]=thisBothJRFPooledSample;
			CountEitherJRFPerSample[eventKey]=thisCountEitherJRFPerSample
			IncExcReadsPooledSample[eventKey]=thisIncExcReadPooledSample
			CountIncExcReadsPerSample[eventKey]=thisCountIncExcReadsPerSample
			CoBound[eventKey]=thisCoBound;
			linesCriteria[eventKey]=thisCriteria;
		#else:
		#	#print >> sys.stderr, "adding eventkeyed="+eventKey; #line not in yet, no choice, has to add
		#	linesMem[eventKey]=lin;
		#	linesCriteria[eventKey]=thisCriteria;	
		#	linesJRFFlag[eventKey]=thisJRFlag;
		#	linesBoundFlag[eventKey]=thisCoBound;

	fin.close();

	#now output the lines memorized:
	keyed=sorted(linesMem.keys());	#go by sorted key!
	
	
	#lines=linesMem.values();
	
	print >> sys.stderr, str(len(keyed))+" uniq events keyed";	

	for _key in keyed:
		print >> sys.stdout, linesMem[_key];




try:
	filename,startRow,idCols,inJRFCols,exJRFCols,incExcReadCols,NICols,NECols,pvalueCols,ThresholdBothJRFAllEvent,ThresholdEitherJRFPerEvent, ThresholdSumIncExcReadsPooledSample,ThresholdIncExcReadsPerSample,favorFlankingCobound,criteria=sys.argv[1:]
except:
	print >>sys.stderr, "Usage: "+sys.argv[0]+" filename startRow1 idCols inJRFCols exJRFCols incExcReadCols NICols NECols pvalueCols ThresholdBothJRFPooledSample=-1|t ThresholdEitherJRFPerSample=-1|t ThresholdSumIncExcReadsPooledSample=-1|t ThresholdIncExcReadsPerSample=-1|t favorFlankingCobound=no|CoboundCol criteria=mmp:mininmize(min(p-value))|xmp: maximize(min(p-value))|mxp: minimize(max(p-value))|xxp: maximize(max(p-value)) |t:totalNINE ";
	sys.exit()



startRow=int(startRow)	
fs="\t"
header,prestarts=getHeader(filename,startRow-1,startRow,fs)	

ThresholdBothJRFAllEvent=int(ThresholdBothJRFAllEvent)
ThresholdEitherJRFPerEvent=int(ThresholdEitherJRFPerEvent)
ThresholdSumIncExcReadsPooledSample=int(ThresholdSumIncExcReadsPooledSample)
ThresholdIncExcReadsPerSample=int(ThresholdIncExcReadsPerSample)
	
idCols=getCol0ListFromCol1ListStringAdv(header,idCols)
inJRFCols=getCol0ListFromCol1ListStringAdv(header,inJRFCols)
exJRFCols=getCol0ListFromCol1ListStringAdv(header,exJRFCols)
incExcReadCols=getCol0ListFromCol1ListStringAdv(header,incExcReadCols)
NICols=getCol0ListFromCol1ListStringAdv(header,NICols)
NECols=getCol0ListFromCol1ListStringAdv(header,NECols)
pvalueCols=getCol0ListFromCol1ListStringAdv(header,pvalueCols)

print >> stderr, "idCols",getVectorByIndexVector(header,idCols)
print >> stderr, "inJRCols",getVectorByIndexVector(header,inJRFCols)
print >> stderr, "exJRFCols",getVectorByIndexVector(header,exJRFCols)
print >> stderr, "incExcReadCols",getVectorByIndexVector(header,incExcReadCols)
print >> stderr, "NICols",getVectorByIndexVector(header,NICols)
print >> stderr, "NECols",getVectorByIndexVector(header,NECols)
print >> stderr, "pvalueCols",getVectorByIndexVector(header,pvalueCols)
	
if favorFlankingCobound.lower() in ['no','n','f']:
	favorFlankingCobound=-1
else:
	favorFlankingCobound=getCol0ListFromCol1ListStringAdv(header,favorFlankingCobound)[0]	
	print >> stderr, "favorFlankingCobound",getVectorByIndexVector(header,[favorFlankingCobound])

filterSameEvent(filename,startRow,idCols,inJRFCols,exJRFCols,incExcReadCols,NICols,NECols,pvalueCols,ThresholdBothJRFAllEvent,ThresholdEitherJRFPerEvent, ThresholdSumIncExcReadsPooledSample,ThresholdIncExcReadsPerSample,favorFlankingCobound,criteria)
