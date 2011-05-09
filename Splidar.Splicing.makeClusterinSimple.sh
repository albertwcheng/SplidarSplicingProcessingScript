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

folders=(`cat $manifestFile`)

tojoin=""

for((i=0;i<${#folders[@]};i++)); do
	mkdir.py $outputDir/$i
	folder=${folders[$i]}
	cuta.py -f.eventType,.eventID,.egstring,.inc/excBound,@\\.Psi$,@.Inc\\+ExcReads$ $folder/$tableBasename > $outputDir/$i/table.txls
	if [ $i == 0 ]; then
		cuta.py -f.eventType,.eventID,.egstring,.inc/excBound $outputDir/$i/table.txls > $outputDir/0/checkCols
	else
		cuta.py -f.eventType,.eventID,.egstring,.inc/excBound $outputDir/$i/table.txls > $outputDir/$i/checkCols
		diff -s -q $outputDir/$i/checkCols $outputDir/0/checkCols
	fi
 	
 	tojoin="$tojoin $outputDir/$i/table.txls"


done

#now join
rm $outputDir/merged.table.txls
mjcmd="multijoinu.sh \"-1 1-4 -2 1-4\" $outputDir/merged.table.txls $tojoin"
eval $mjcmd

#colStat.py $outputDir/merged.table.txls

awk -v FS="\t" -v OFS="\t" '$0!~/nan/' $outputDir/merged.table.txls > $outputDir/merged.table.noNAN.txls

#now filter incExcReads
pyFilter.py $outputDir/merged.table.noNAN.txls "min([@Inc\\+ExcReads$])>=$incExcReadsMin and max([@\\.Psi$])-min([@\\.Psi$])>=$RangeMin" > $outputDir/merged.table.incExcReadsge$incExcReadsMin.rangege$RangeMin.txls

cuta.py -f.eventID,@\\.Psi$ $outputDir/merged.table.incExcReadsge$incExcReadsMin.rangege$RangeMin.txls > $outputDir/merged.table.incExcReadsge$incExcReadsMin.rangege$RangeMin.clusterin
