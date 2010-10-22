

mkdir ../Combined
mkdir ../Combined/Genes

FDRSelector='@TFFDR$'
dPsiSelector='@dPsi$'
threshold=0.05


echo "file events genes" > ../Combined/combineEvent.log


tocopy[1]=CombinedAnalysis.final.FDRm.Detectable.xls
tocopy[2]=CombinedAnalysis.final.FDRm.DetectedBoth.xls
tocopy[3]=CombinedAnalysis.final.FDRm.DetectedBoth.FDR0.05.xls
tocopy[4]=CombinedAnalysis.final.FDRm.DetectedBoth.FDR0.05_dPsi-0.10.1.xls
tocopy[5]=CombinedAnalysis.final.FDRm.DetectedBoth.FDR0.05_dPsi-0.30.3.xls
tocopy[6]=CombinedAnalysis.final.FDRm.DetectedBoth.FDR0.05_dPsi-0.10.1bps_union.xls
tocopy[7]=CombinedAnalysis.final.FDRm.DetectedBoth.FDR0.05_dPsi-0.30.3bps_union.xls
tocopy[8]=CombinedAnalysis.final.FDRm.DetectedBoth.FDR0.05bps_union.xls

newgeneprefix="../Combined/Genes/"

allprefix="../Combined/all."


for tocop in ${tocopy[@]}; do
	if [ -e $allprefix$tocop ]; then
		rm $allprefix$tocop
	fi
done

#if [ -e ${allprefix}CombinedAnalysis.final.FDRm.FDR$threshold.xls ]; then
#	rm ${allprefix}CombinedAnalysis.final.FDRm.FDR$threshold.xls
#fi

for event in RI SE MXE A5SS A3SS  A3UTR AFE  ALE; do #
	eventRoot="../$event/byEGString/ensRemapped/"
	newprefix="../Combined/$event."
	

	for tocop in ${tocopy[@]}; do
		cp $eventRoot/$tocop $newprefix$tocop
		if [ ! -e $allprefix$tocop ]; then
			cat $eventRoot/$tocop >> $allprefix$tocop
		else
			awk 'FNR>1' $eventRoot/$tocop >> $allprefix$tocop	
		fi
	done



	
	#combinedanalysisfilepath="$eventRoot/CombinedAnalysis.final.FDRm.xls"
	#colFDR=`colSelect.py $combinedanalysisfilepath $FDRSelector`	
	#echo "selected colFDR=" $colFDR >> /dev/stderr
	#awk -v colFDR=$colFDR -v THRESHOLD=$threshold 'BEGIN{OFS="\t";FS="\t"}(FNR==1 || $colFDR<THRESHOLD)' $combinedanalysisfilepath > ${newprefix}CombinedAnalysis.final.FDRm.FDR$threshold.xls
	#if [ ! -e ${allprefix}CombinedAnalysis.final.FDRm.FDR$threshold.xls ]; then
	#	cat ${newprefix}CombinedAnalysis.final.FDRm.FDR$threshold.xls >> ${allprefix}CombinedAnalysis.final.FDRm.FDR$threshold.xls
	#else
	#	awk 'FNR>1' ${newprefix}CombinedAnalysis.final.FDRm.FDR$threshold.xls >> ${allprefix}CombinedAnalysis.final.FDRm.FDR$threshold.xls
	#fi
	#oripath=`pwd`
	


	

done

bash combineEvents_moreC.sh

for i in ../Combined/*.xls; do
	numevents=`wc -l $i | cut -d" " -f1`
	#echo $i has $numevents rows
	numevents=`expr $numevents - 1` #discount header
	echo $i has $numevents events >> /dev/stderr
		
	bas=`basename $i`
	getUniqueNameFromTable.sh $i .locusName 2 > $newgeneprefix/${bas/.xls/}.genenames.txt
	numgenes=`wc -l $newgeneprefix/${bas/.xls/}.genenames.txt | cut -d" " -f1`
	echo $i has $numgenes genes >> /dev/stderr
	echo $i $numevents $numgenes >> ../Combined/combineEvent.log
done

#bash getMappingToFusedGenes.sh all.CombinedAnalysis.final.FDRm.Detectable.xls ../Combined/


