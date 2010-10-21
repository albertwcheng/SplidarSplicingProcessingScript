#!/usr/bin/python

#  1.  chrom - The name of the chromosome (e.g. chr3, chrY, chr2_random) or scaffold (e.g. scaffold10671).
#   2. chromStart - The starting position of the feature in the chromosome or scaffold. The first base in a chromosome is numbered 0.
#   3. chromEnd - The ending position of the feature in the chromosome or scaffold. The chromEnd base is not included in the display of the feature. For example, the first 100 bases of a chromosome are defined as chromStart=0, chromEnd=100, and span the bases numbered 0-99. 

#The 9 additional optional BED fields are:

#   4. name - Defines the name of the BED line. This label is displayed to the left of the BED line in the Genome Browser window when the track is open to full display mode or directly to the left of the item in pack mode.
#   5. score - A score between 0 and 1000. If the track line useScore attribute is set to 1 for this annotation data set, the score value will determine the level of gray in which this feature is displayed (higher numbers = darker gray). This table shows the Genome Browser's translation of BED score values into shades of gray:
#      shade 	  	  	  	  	  	  	  	  	 
#   6. strand - Defines the strand - either '+' or '-'.
#   7. thickStart - The starting position at which the feature is drawn thickly (for example, the start codon in gene displays).
#   8. thickEnd - The ending position at which the feature is drawn thickly (for example, the stop codon in gene displays).
#   9. itemRgb - An RGB value of the form R,G,B (e.g. 255,0,0). If the track line itemRgb attribute is set to "On", this RBG value will determine the display color of the data contained in this BED line. NOTE: It is recommended that a simple #color scheme (eight colors or less) be used with this attribute to avoid overwhelming the color resources of the Genome Browser and your Internet browser.
#  10. blockCount - The number of blocks (exons) in the BED line.
#  11. blockSizes - A comma-separated list of the block sizes. The number of items in this list should correspond to blockCount.
#  12. blockStarts - A comma-separated list of block starts. All of the blockStart positions should be calculated relative to chromStart. The number of items in this list should correspond to blockCount. 

import sys
from sys import stderr,stdout,exit
from albertcommon import *
from getopt import getopt

def getVectorByIndexVector(datavector,indexvector):
	v=[]
	for idx in indexvector:
		v.append(datavector[idx])

	return v

def StringVectorToIntVectorInPlace(V):
	for i in range(0,len(V)):
		V[i]=int(V[i])	


programName=sys.argv[0]
opts,args=getopt(sys.argv[1:],'',['track-name=','item-sep=','block-sep=','startRow=','col-sep=','colors='])

if len(args)!=5:
	print >> stderr, args
	print >> stderr,programName,"filename nameCols chromCols strandCols coordinateCols"
	exit()

filename,nameCols,chromCols,strandCols,coordinateCols=args



trackName=filename
itemSep="/"
blockSep=","
startRow=2
colSep="\t"
nameJoinSep="."
coordSep="-"
colors=[]

for a,v in opts:
	if a=="--track-name":
		trackName=v
	elif a=="--item-sep":
		itemSep=v
	elif a=="--block-sep":
		blockSep=v
	elif a=="--startRow":
		startRow=int(v)
	elif a=="--col-sep":
		colSep=v
	elif a=="--coord-sep":
		coordSep=v
	elif a=="--name-join-sep":
		nameJoinSep=v
	elif a=="--colors":
		colors=v.split("_")

headerRow=startRow-1

header,prestarts=getHeader(filename,headerRow,startRow,colSep)


nameCols=getCol0ListFromCol1ListStringAdv(header,nameCols)
chromCols=getCol0ListFromCol1ListStringAdv(header,chromCols)
strandCols=getCol0ListFromCol1ListStringAdv(header,strandCols)
coordinateCols=getCol0ListFromCol1ListStringAdv(header,coordinateCols)

#now the real deal
fin=open(filename)

print >> stdout,"track name=\""+trackName+"\" description=\""+trackName+"\" useScore=0 itemRgb=On visibility=full"

lino=0
for line in fin:
	lino+=1
	if lino<startRow:
		continue	

	line=line.rstrip("\r\n")
	fields=line.split(colSep)
	name=nameJoinSep.join(getVectorByIndexVector(fields,nameCols))
	itemIndex=0	
	for chromCol,strandCol,coordinateCol in zip(chromCols,strandCols,coordinateCols):
		chrom=fields[chromCol]
		strand=fields[strandCol]
		coordinate=fields[coordinateCol]
		items=coordinate.split(itemSep)
		for item in items:
			itemIndex+=1
			itemString=[]
			blocks=item.split(blockSep)
			blockBounds=[]
			itemMin=10000000000
			itemMax=-10000000000

			for block in blocks:
				blockSplit=block.split(coordSep)
				StringVectorToIntVectorInPlace(blockSplit)
				if len(blockSplit)<2:
					blockBounds.append([blockSplit[0],blockSplit[0]])
				else:
					thisMin=min(blockSplit[0],blockSplit[1])	
					thisMax=max(blockSplit[0],blockSplit[1])		
					blockBounds.append([thisMin,thisMax])
					itemMin=min(thisMin,itemMin)
					itemMax=max(thisMax,itemMax)
			
			if len(colors)==0:
				color="0,0,0"
			else:
				color=colors[itemIndex-1]
			
			itemString.extend([chrom,str(itemMin-1),str(itemMax),name+nameJoinSep+str(itemIndex),"0",strand,str(itemMin-1),str(itemMax),color,str(len(blockBounds))])
			
			blockBoundStartMap=dict()
			for blockBound in blockBounds:
				blockBoundStartMap[blockBound[0]]=blockBound
			
			blockStartSorted=blockBoundStartMap.keys()
			blockStartSorted.sort()

			blockSizes=[]
			blockStarts=[]

			for blockStart in blockStartSorted:
				blockBound=blockBoundStartMap[blockStart]
				blockSizes.append(str(int(blockBound[1])-int(blockBound[0])+1))
				blockStarts.append(str(int(blockBound[0])-itemMin))

			itemString.extend([",".join(blockSizes),",".join(blockStarts)])
			
			print >> stdout," ".join(itemString)

				
			
			
	


fin.close()






