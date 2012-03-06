#!/bin/bash

if [ $# -lt 3 ];then
	echo $0 columnsSpec eventsSpec rootDir outputDir
	echo "if spec files not present in current dir, the path specified in \$SETTINGPATH ($SETTINGPATH) will be used."
	echo "e.g., Splidar.Splicing.MakeSummaryTables.sh columnSpec.txt eventsSpec.txt splidar-Splicing-m splidar-Splicing-m.summaryTables"
	exit
fi

columnsSpec=$1

if [ ! -e $columnsSpec ]; then
	if [ ! -e $SETTINGPATH/$columnsSpec ]; then
		echo columnsSpec not exist
		echo abort
		exit
	fi
	columnsSpec=$SETTINGPATH/$columnsSpec
fi

eventsSpec=$2

if [ ! -e $eventsSpec ]; then
	if [ ! -e $SETTINGPATH/$eventsSpec ]; then
		echo eventsSpec not exist
		echo abort
		exit
	fi
	eventsSpec=$SETTINGPATH/$eventsSpec
fi

rootDir=$3
outputDir=$4

eventSubFolder=byEGString
leftCornerLabel=eventType

mkdir.py $outputDir

saveIFS=$IFS
IFS=":"
colLabels=(`cuta.py -f1 $columnsSpec | tr "\n" ":"`)
colFiles=(`cuta.py -f2 $columnsSpec | tr "\n" ":"`)

rowLabels=(`cuta.py -f1 $eventsSpec | tr "\n" ":"`)
rowFolders=(`cuta.py -f2 $eventsSpec | tr "\n" ":"`)

IFS=$saveIFS

for((y=0;y<${#rowLabels[@]};y++)); do
	rowLabel=${rowLabels[$y]}
	rowFolder=${rowFolders[$y]}
	echo processing events $rowLabel
	for comparisonFolder in $rootDir/$rowFolder/$eventSubFolder/*; do
		if [ ! -e $comparisonFolder/CombinedAnalysis.final.FDRm.Detectable.xls ]; then
			continue; #not a proper folder, skip
		fi
		comparisonName=`basename $comparisonFolder`
		echo -e "\t-" $comparisonName
		if [ $y == 0 ]; then
			mkdir.py $outputDir/$comparisonName
			rm -f $outputDir/$comparisonName/tmp.00 #clear that that will contain the temp data
		fi
		
		for((x=0;x<${#colLabels[@]};x++)); do
			colLabel=${colLabels[$x]}
			theFileBN=${colFiles[$x]}
			theFile=$comparisonFolder/$theFileBN
			numRows=`cat $theFile | wc -l`
			numItems=`expr $numRows - 1`
			#now output that to XYZRows File
			echo -e "$colLabel\t$rowLabel\t$numItems" >> $outputDir/$comparisonName/tmp.00
		done
		
	
	done
done


for subF in $outputDir/*; do
	XYZRowsToZOnXYMatrix.py --left-corner $leftCornerLabel $subF/tmp.00 > $subF/summaryTable.txls
done