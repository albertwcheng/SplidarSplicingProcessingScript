#!/bin/bash

if [ $# -lt 3 ]; then
	echo $0 eventebed chain outFile
	exit
fi

eventebed=$1
chain=$2
outFile=$3

#first convert to genePred
ebed2GenePred.py --fs " " $eventebed > $outFile.gp.00

#now liftover!
liftOver -genePred $outFile.gp.00 $chain $outFile.over.gp.00 $outFile.over.gp.unmapped.00

#now convert back to ebed
ebed2GenePred.py --genePred2ebed $outFile.over.gp.00 > $outFile.00

#now need to filter those events both isoform retained
Splidar.Splicing.Comparative.liftOverEvents.filterBothRetained.py $outFile.00 > $outFile