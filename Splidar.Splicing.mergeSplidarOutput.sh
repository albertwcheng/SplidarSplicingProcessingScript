#!/bin/bash

#chmod 777 *.sh
#chmod 777 *.py

if [ $# -lt 2 ]; then
	echo $0 genome eventType > /dev/stderr
	exit
fi

genome=$1
eventType=$2

LD_LIBRARY_PATH=/usr/local/lib
export LD_LIBRARY_PATH

fPrintTestPath=ftestPrint

scriptDir=`pwd`

rm *.00

cd ..


rm -f *.00
rm -f seq.merged.highlyRedundant

rootDir=`pwd`



cd $scriptDir

source $scriptDir/params.sh
#echo $filterEventCriteria

cd $scriptDir

manifestfile=../manifest.txt

TAB=`echo -e "\t"`


if [ ! -e  $manifestfile ]; then
	echo "manifest.txt does not exist. Create one and put sample name in it" > /dev/stderr
	exit;
fi;

samplesString=`cat "$manifestfile"`

samples=($samplesString)

nSamples=${#samples[@]}

templateSample=${samples[0]}

echo "There are $nSamples samples"
echo "They are ${samples[@]}"

#if [ 1 -eq 0 ]; then

#clean stuff

if [ -e ../Events.count.log ]; then
	rm ../Events.count.log
fi

#now merge sequence file using the first sample as template:
$scriptDir/mergeSplidarOutputSeq.sh $scriptDir $rootDir $templateSample
#now there should be eventID.00 and seq.headless.00  and eventKey.00 here!!

#check alignment of events:
#header:
#eventID	eventType	locusName	egstring	jnxstring	chr	strand	inc/excBound	flankingCoboundFlag	inc/excCompleteBound	incSpecBound	excSpecBound	UCSCGenomeBrowser	sampleLabel.inFXR	inFXP	sampleLabel.inJR	inJP	sampleLabel.inMXR	inMXP	sampleLabel.inJRCheckString	inJPCheckString	sampleLabel.inJRFlag	inJPFlag	sampleLabel.exFXR	exFXP	sampleLabel.exJR	exJP	sampleLabel.exMXR	exMXP	sampleLabel.exJRCheckString	exJPCheckString	sampleLabel.exJRFlag	exJPFlag	sampleLabel.IncReads	IncPos	sampleLabel.ExcReads	ExcPos	sampleLabel.Inc+ExcReads	sampleLabel.NI	sampleLabel.NE+	sampleLabel.IR	sampleLabel.IncDensity	sampleLabel.ExcDensity	sampleLabel.Psi

for sample in ${samples[@]}; do
	$scriptDir/mergeSplidarOutputPerSample.sh $scriptDir $rootDir $sample $genome
	#now check if the event keys are aligned
	diffResult=`diff -q -s "$rootDir/$sample/$sample.eventKey.00" $rootDir/eventKey.00`
	echo $diffResult > /dev/stderr
	if [[ $diffResult =~ "diff" ]]; then
		echo "event Not aligned. abort" > /dev/stderr
		exit;
	fi 
done;

#now everything is fine
echo "events are aligned properly" > /dev/stderr

#now merge!
cuta.py -f .eventID-.UCSCGenomeBrowser,.inFXP,.inJP,.inMXP,.inJPCheckString,.inJPFlag,.exFXP,.exJP,.exMXP,.exJPCheckString,.exJPFlag,.IncPos,.ExcPos $rootDir/$templateSample/$templateSample.merged.xls > $rootDir/tmp.00

#this is the event info portion to tmp.00

for sample in ${samples[@]}; do
	cuta.py -f "@$sample" $rootDir/$sample/$sample.merged.xls > $rootDir/t.00 #sample-specific info, like counts, stuff
	#the following three lines are simply tmp.00+=t.00
	paste $rootDir/tmp.00 $rootDir/t.00 > $rootDir/tmp2.00 
	rm $rootDir/tmp.00
	mv $rootDir/tmp2.00 $rootDir/tmp.00
done;

#rename tmp.00 to Combined-1.00 that contains (with header) the info, followed by each sample's data
mv $rootDir/tmp.00 $rootDir/Combined-1.00

IRColsString=`colSelect.py "$rootDir/Combined-1.00" @.IR`
PsiColsString=`colSelect.py "$rootDir/Combined-1.00" @.Psi`
NIColsString=`colSelect.py "$rootDir/Combined-1.00" @.NI`
NEColsString=`colSelect.py "$rootDir/Combined-1.00" @.NE+`

IRCols=($IRColsString)
PsiCols=($PsiColsString)
NICols=($NIColsString)
NECols=($NEColsString)

#selectors for columns of IR, Psi, NI and NE's
nIRCols=${#IRCols[@]}
nPsiCols=${#PsiCols[@]}
nNICols=${#NICols[@]}
nNECols=${#NECols[@]}

if [[ $nIRCols != $nSamples ]] || [[ $nPsiCols != $nSamples ]] || [[ $nNICols != $nSamples ]] || [[ $nNECols != $nSamples ]] ; then
	echo "weird: sample numbers != number of Psi or IR cols or NI cols or NE+ cols. Abort"
	exit
fi


#pairwise dIR and dPsi
awk -f delta.awk -v NAME=dPsi -v COLS="$PsiColsString" -v COLNAMES="$samplesString" $rootDir/Combined-1.00 > $rootDir/dPsi.00
awk -f delta.awk -v NAME=dIR -v COLS="$IRColsString" -v COLNAMES="$samplesString" $rootDir/Combined-1.00 > $rootDir/dIR.00



combined100Len=`wc -l $rootDir/Combined-1.00 | cut -d" " -f1`
#calculate fischer for pairwise sample into sample1_sample2.fisher.00
for((i=0;i<nSamples-1;i++)); do
	for((j=i+1;j<nSamples;j++)); do
		#NI[1] NI[2] NE[1] NE[2] startRow=2
		echo ${samples[$j]}-${samples[$i]}.fisherpvalue > "$rootDir/${i}_${j}.fisher.00"
		$fPrintTestPath $rootDir/Combined-1.00 ${NICols[$i]} ${NICols[$j]} ${NECols[$i]} ${NECols[$j]} 2 >> "$rootDir/${i}_${j}.fisher.00" 2> /dev/null
		fisher00Len=`wc -l $rootDir/${i}_${j}.fisher.00 | cut -d" " -f1`
		#echo $fisher00Len
		#echo $combined100Len
		if [ $fisher00Len != $combined100Len ]; then

			echo "error: fisher len != combined len"
			exit
		fi
	done
done

#paste all pairwise fisher together
paste $rootDir/*.fisher.00 > $rootDir/fisher.00

#now past everything together into CombinedAnalysis.highlyRedundant
paste $rootDir/Combined-1.00 $rootDir/dPsi.00 $rootDir/dIR.00 $rootDir/fisher.00 > $rootDir/CombinedAnalysis.highlyRedundant

if [ -e $rootDir/byEGString ]; then
	rm -R $rootDir/byEGString
fi

if [ -e $rootDir/byJxString ]; then
	rm -R $rootDir/byJxString
fi



mkdir $rootDir/byEGString
#mkdir $rootDir/byJxString




#Usage: filterUniqueEventsMulti.py filename startRow1 idCols inJRFCols exJRFCols incExcReadCols NICols NECols pvalueCols ThresholdBothJRFPooledSample=-1|t ThresholdEitherJRFPerSample=-1|t ThresholdSumIncExcReadsPooledSample=-1|t ThresholdIncExcReadsPerSample=-1|t favorFlankingCobound=no|CoboundCol criteria=mmp:mininmize(min(p-value))|xmp: maximize(min(p-value))|mxp: minimize(max(p-value))|xxp: maximize(max(p-value)) |t:totalNINE 

#select unique event by EGString selecting the one with both events JRFlag and maximize NE+NI total or pvalue
$scriptDir/filterUniqueEventsMulti.py $rootDir/CombinedAnalysis.highlyRedundant 2 .locusName,.egstring @inJRFlag @exJRFlag "@Inc\\+ExcReads" @NI @NE+ @fisherpvalue $ThresholdBothJRFPooledSample $ThresholdEitherJRFPerSample $ThresholdSumIncExcReadsPooledSample $ThresholdIncExcReadsPerSample $favorFlankingCobound  $filterEventCriteria > $rootDir/byEGString/Combined.00

#fi #the if [ 1 -eq 0 ]

echo "do with Exon group collapsed file"
###ThresholdIncExcReadsPerSample=$6
##ThresholdSumIncExcReadsSamplePair=$7
##incDetectionThreshold=$8
##excDetectionThreshold=$9
##JFThreshold=${10}
##FDRThreshold=${11}
$scriptDir/mergeSplidarOutput_postCollapse.sh $scriptDir $rootDir byEGString $genome $eventType #$ThresholdIncExcReadsPerSample $ThresholdSumIncExcReadsSamplePair $incDetectionThreshold $excDetectionThreshold $JFThreshold $FDRThreshold


#echo "do with jnx string collapsed file"
###
#$scriptDir/mergeSplidarOutput_postCollapse.sh $scriptDir $rootDir byJxString $genome $eventType $TFThreshold $JFThreshold

cd $scriptDir
#remove or not??
#rm *.00
echo "<Done Processing>"

