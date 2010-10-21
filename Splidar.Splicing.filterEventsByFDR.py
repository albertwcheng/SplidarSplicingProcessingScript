#!/usr/bin/python


import sys;
from math import fabs;



def NAFloat(S,naValue):
	if S=="nan":
		return naValue
	else:
		return float(S)

def filterEventByFDR(filename, startRow1, pvalCol1, FDRThreshold, dPsiCol1, dPsiAbsLBi, dIRCol1, dIRAbsLBi):
	fin=open(filename);
	
	pvalCol0=pvalCol1-1;
	dPsiCol0=dPsiCol1-1;
	dIRCol0=dIRCol1-1;

	linesMem=[];
	linespValue=[];
	dPsiAbs=[];
	dIRAbs=[];


	lino=0;
	for lin in fin:
		lino+=1;
		lin=lin.strip();
		spliton=lin.split("\t");

		if(lino<startRow1):
			print >> sys.stdout, lin;
			continue;
		

		thisPvalue=NAFloat(spliton[pvalCol0],1.0);
		linesMem.append(lin);	
		linespValue.append(thisPvalue);
		dPsiAbs.append(fabs(float(spliton[dPsiCol0])));
		dIRAbs.append(fabs(float(spliton[dIRCol0])));
		

	fin.close();

	#now compute pvalue-cutoff
	sortedpvalue=sorted(linespValue);
	nItems=len(sortedpvalue);
	pvalue=0;
	observed=0;
	pvalueThr=0;
	neverSet=True;
	for thispvalue in sortedpvalue:
		observed+=1;		
		pvalueThr=thispvalue;
		predFalse=float(nItems)*thispvalue;
		thisFDR=predFalse/float(observed);
		print >>sys.stderr,"pvalue="+str(thispvalue)+",predFalse="+str(predFalse)+"/"+str(nItems)+",observed="+str(observed)+",thisFDR="+str(thisFDR);
		if(thisFDR>FDRThreshold):
			neverSet=False;			
			break;
	
	if(neverSet):
		pvalueThr+=0.01;	#add an arbituary value so to include the last entry
	
	print >>sys.stderr, "pvalue < "+str(pvalueThr)+" for FDR < "+str(FDRThreshold);


	#now output the lines memorized:
	
	
	print >> sys.stderr, str(len(linesMem))+" line(s)";

	linesWritten=0;
	for i in range(0,nItems):
		thisPvalue=linespValue[i];
		if(thisPvalue>=pvalueThr):
			continue; #skip this line p-value not acceptable for the FDR threshold
		
		thisdPsiAbs=dPsiAbs[i];
		if(thisdPsiAbs<dPsiAbsLBi):
			continue; #skip this line dPsi not acceptable

		thisdIRAbs=dIRAbs[i];
		if(thisdIRAbs<dIRAbsLBi):
			continue; #skip this line dIR not acceptable	
		linesWritten+=1;
		print >> sys.stdout, linesMem[i];
		
	print >> sys.stderr, "<Done>:"+str(linesWritten)+" lines written";


if(len(sys.argv)<9):
	print >>sys.stderr, "Usage: "+sys.argv[0]+" filename startRow1 pvalCol1 FDRThreshold dPsiCol1 dPsiAbsLBi dIRCol1 dIRAbsLBi";
else:
	filterEventByFDR(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]),float(sys.argv[6]),int(sys.argv[7]),float(sys.argv[8]));
