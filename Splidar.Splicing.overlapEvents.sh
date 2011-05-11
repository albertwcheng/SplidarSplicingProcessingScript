#!/bin/bash

if [ $# -lt 3 ]; then
	echo $0 setting.shvar manifest outputdir
	exit
fi

settingShvar=$1
manifestFile=$2
outputDir=$3

mkdir.py $outputDir

source $settingShvar

comparisons=(`cuta.py -f1 $manifestFile`)
files=(`cuta.py -f2 $manifestFile`)


toCompareEventTLocusEGString=""
toCompareEventTLocus=""
toCompareEventTID=""

for((i=0;i<${#comparisons[@]};i++)); do
	
	file=${files[$i]}
	comparison=${comparisons[$i]}
	
	mkdir.py $outputDir/$comparison
	
	cuta.py -f.eventType,.locusName,.egstring $file > $outputDir/$comparison/$comparison.eventTLocusEGString.txt
	cuta.py -f.eventType,.locusName $outputDir/$comparison/$comparison.eventTLocusEGString.txt > $outputDir/$comparison/$comparison.eventTLocus.txt
	cuta.py -f.eventType,.eventID $file > $outputDir/$comparison/$comparison.eventTID.txt
 	
 	toCompareEventTLocusEGString="$toCompareEventTLocusEGString $outputDir/$comparison/$comparison.eventTLocusEGString.txt"
 	toCompareEventTLocus="$toCompareEventTLocus $outputDir/$comparison/$comparison.eventTLocus.txt"
 	toCompareEventTID="$toCompareEventTID $outputDir/$comparison/$comparison.eventTID.txt"


done

#now listCount

listCount.py --headerFrom1To 1 --remove-ext-on-stdout-labels --usebasename --outcombination $outputDir/$comparison/,.comb.txls $toCompareEventTLocusEGString > $outputDir/CompareEventTLocusEGString.txls
listCount.py --headerFrom1To 1 --remove-ext-on-stdout-labels --usebasename --outcombination $outputDir/$comparison/,.comb.txls $toCompareEventTLocus > $outputDir/CompareEventTLocus.txls
listCount.py --headerFrom1To 1 --remove-ext-on-stdout-labels --usebasename --outcombination $outputDir/$comparison/,.comb.txls $toCompareEventTID > $outputDir/CompareEventTID.txls
