#!/bin/bash

TAB=`echo -e "\t"`;

if [ $# -lt 6 ]; then
	echo "ERROR post collapse received insufficient arguments"
	exit
fi

scriptDir=$1
rootDir=$2
prefix=$3
genome=$4
eventType=$5
paramfile=$6

source $paramfile

cd $rootDir



echo "$prefix>" >> Events.count.log

#now get the sequence simplified;
cut -d"$TAB" -f1 "$prefix/Combined.00" | sort -k1,1 > "$prefix/seq.request.00"
join -t"$TAB" "$prefix/seq.request.00" seq.merged.highlyRedundant > "$prefix/seq.merged.00"

cat $scriptDir/Splidar.Splicing.seqHeader.txt "$prefix/seq.merged.00" > "$prefix/seq.merged.xls"

getNamesDesc.py --nameout "$prefix/CombinedAnalysis.names" $genome.config "$prefix/Combined.00" 3  3 > "$prefix/CombinedAnalysis.final.all.xls" 2> "$prefix/getGO.log"

#wc -l "$prefix/CombinedAnalysis.final.all.xls" >> Events.count.log


#fileName,ThresholdIncExcReadsPerSample,ThresholdSumIncExcReadsSamplePair,incDetectionThreshold,excDetectionThreshold,JRThreshold
Splidar.Splicing.SplidarAddFlag.py "$prefix/Combined.00" $ThresholdIncExcReadsPerSample $ThresholdSumIncExcReadsSamplePair $incDetectionThreshold $excDetectionThreshold $JFThreshold > "$prefix/CombinedAnalysis.final.FDRm.00" 

Splidar.Splicing.EventBEDMaker.py --track-name $eventType --colors "255,0,0_0,0,255" "$prefix/CombinedAnalysis.final.FDRm.00" .eventType,.locusName,.eventID .chr .strand ".inc/excBound" > "$prefix/CombinedAnalysis.final.FDRm.BED" 

Splidar.Splicing.EventBEDMaker.py --track-name $eventType --colors "255,0,0_0,0,255" "$prefix/CombinedAnalysis.final.FDRm.00" .eventType,.locusName,.eventID .chr .strand ".inc/excCompleteBound" > "$prefix/CombinedAnalysis.final.FDRm.CompleteBound.BED" 


###
##
#  merge things and anotate!
## 


#paste totalFlow.DB.FDR.00 JRFlag.DB.FDR.00 > FDR.m.00
#echo -e "minFDR\nUnion" > union.00
#awk -F"\t" '(FNR>2) {if($1<$2){print $1}else{print $2}}' FDR.m.00 >> union.00
#echo -e "maxFDR\nIntersection" > intersect.00
#awk -F"\t" '(FNR>2) {if($1>$2){print $1}else{print $2}}' FDR.m.00 >> intersect.00

#paste ../Combined.00 totalFlow.Detectable.00 totalFlow.Detected.00 totalFlow.DetectedBoth.00 totalFlow.DB.FDR.00 JRFlag.Detectable.00 JRFlag.Detected.00 JRFlag.DetectedBoth.00 JRFlag.DB.FDR.00 union.00 intersect.00 > CombinedAnalysis.final.FDRm.00 


getNamesDesc.py --nameout $prefix/CombinedAnalysis.final.FDRm.names $genome.config $prefix/CombinedAnalysis.final.FDRm.00 3 2 > $prefix/CombinedAnalysis.final.FDRm.xls 2> "$prefix/getGO.log"

bgsetOrig=$prefix/CombinedAnalysis.final.FDRm.xls


colDetectable=`colSelect.py -o, $bgsetOrig $detectableColSelector`  #121,122,123,124,125,126
colDetected=`colSelect.py -o, $bgsetOrig $detectedColSelector`
colDetectedBoth=`colSelect.py -o, $bgsetOrig $detectedbothColSelector`
FDRColSelector=`colSelect.py -o, $bgsetOrig @TFFDR$`
dPsiColSelector=`colSelect.py -o, $bgsetOrig @dPsi$`

head -n 1 $bgsetOrig > bgsethead.00

echo colDetectable = $colDetectable `cuta.py -f$colDetectable bgsethead.00`
echo colDetected = $colDetected `cuta.py -f$colDetected bgsethead.00`
echo colDetectedBoth = $colDetectedBoth `cuta.py -f$colDetectedBoth bgsethead.00`



sampleComparisons=`cuta.py -f$colDetected bgsethead.00 | tr "\t" " " | awk -v FS=" " -v OFS="," '{for(i=1;i<=NF;i++){split($i,a,"."); $i=a[1];} print;}'`
#R3-R2,R4-R2,R5-R2,R4-R3,R5-R3,R5-R4





saveIFS=$IFS
IFS=`echo -en ","`
declare -a colDetecteds=($colDetected)
declare -a colDetectedBoths=($colDetectedBoth)
declare -a sampleComparisons=($sampleComparisons)
declare -a FDRColSelectors=($FDRColSelector)
declare -a dPsiColSelectors=($dPsiColSelector)
IFS=$saveIFS

#now go to each comparison

numComparisons=${#sampleComparisons[@]}

for((i=0;i<numComparisons;i++));do
	#now output the selected sets based on  those fields
	
	sampleComparison=${sampleComparisons[$i]}
	colDetected=${colDetecteds[$i]}
	colDetectedBoth=${colDetectedBoths[$i]}
	FDRColSelector=${FDRColSelectors[$i]}
	dPsiColSelector=${dPsiColSelectors[$i]}

	echo sampleComparison = $sampleComparison
	echo colDetected = $colDetected `cuta.py -f$colDetected bgsethead.00`
	echo colDetectedBoth = $colDetectedBoth `cuta.py -f$colDetectedBoth bgsethead.00`
	echo FDRColSelector = $FDRColSelector `cuta.py -f$FDRColSelector bgsethead.00`
	echo dPsiColSelector = $dPsiColSelector `cuta.py -f$dPsiColSelector bgsethead.00`

	#continue
	
	newprefix=$prefix/$sampleComparison
	mkdir $newprefix

	bgset=$newprefix/CombinedAnalysis.final.FDRm.xls
	detectableout=$newprefix/CombinedAnalysis.final.FDRm.Detectable.xls
	detectedout=$newprefix/CombinedAnalysis.final.FDRm.Detected.xls
	detectedbothout=$newprefix/CombinedAnalysis.final.FDRm.DetectedBoth.xls

	
	cp $bgsetOrig $bgset

	awk -v col=$colDetectable 'BEGIN{OFS="\t";FS="\t"}(FNR==1 || $col>0)' $bgset > $detectableout
	awk -v col=$colDetected 'BEGIN{OFS="\t";FS="\t"}(FNR==1 || $col>0)' $bgset > $detectedout
	awk -v col=$colDetectedBoth 'BEGIN{OFS="\t";FS="\t"}(FNR==1 || $col>0)' $bgset > $detectedbothout


	for dPsiThresholdUpper in 0.0 0.1 0.2 0.3; do
		bash $scriptDir/Splidar.Splicing.findPowerSet.sh $FDRColSelector $FDRThreshold $dPsiColSelector -$dPsiThresholdUpper $dPsiThresholdUpper $bgset $scriptDir
	done

	cd $newprefix

	mkdir names

	echo "$sampleComparison>"  >> $rootDir/Events.count.log

	for fil in *.xls; do
		wc -l $fil >> $rootDir/Events.count.log
		cuta.py -f".locusName" $fil | awk '(FNR>1)' | sort | uniq > names/${fil/.xls/.names.txt} 
	done

	cd $rootDir

done

cat $rootDir/Events.count.log

#rm *.00
#cd ../
#rm *.00
#cd ../
