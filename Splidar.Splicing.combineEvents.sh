

mkdir.py Combined
#mkdir Combined/Genes

FDRSelector='@TFFDR$'
dPsiSelector='@dPsi$'
threshold=0.05


#echo "file events genes" > Combined/combineEvent.log


tocopy[1]=CombinedAnalysis.final.FDRm.Detectable.xls
tocopy[2]=CombinedAnalysis.final.FDRm.DetectedBoth.xls
tocopy[3]=CombinedAnalysis.final.FDRm.FDR0.05.xls
tocopy[4]=CombinedAnalysis.final.FDRm.FDR0.05_dPsi-0.10.1.xls
tocopy[5]=CombinedAnalysis.final.FDRm.FDR0.05_dPsi-0.30.3.xls
tocopy[6]=CombinedAnalysis.final.FDRm.FDR0.05_dPsi-0.10.1bps_union.xls
tocopy[7]=CombinedAnalysis.final.FDRm.FDR0.05_dPsi-0.30.3bps_union.xls
tocopy[8]=CombinedAnalysis.final.FDRm.FDR0.05bps_union.xls




for tocop in ${tocopy[@]}; do
	if [ -e $allprefix$tocop ]; then
		rm $allprefix$tocop
	fi
done


allSEDetectableFiles=(`ls SE/byEGString/*/CombinedAnalysis.final.FDRm.Detectable.xls`)
allComparisons=""

for SEDetectable in ${allSEDetectableFiles[@]}; do
dirn=`dirname $SEDetectable`
comparisonName=`basename $dirn`
allComparisons="$allComparisons $comparisonName"
done

allComparisons=(`echo $allComparisons`)



for event in RI SE MXE A5SS A3SS  A3UTR AFE  ALE; do #
	eventRoot="$event/byEGString/"
	
	for comparison in ${allComparisons[@]}; do
		
		
		
		newprefix="Combined/$comparison/$event."
		newgeneprefix="Combined/$comparison/Genes/"
		allprefix="Combined/$comparison/all."
		
		mkdir.py Combined/$comparison/
		mkdir.py Combined/$comparison/Genes/

		for tocop in ${tocopy[@]}; do
			cp $eventRoot/$comparison/$tocop $newprefix$tocop
			if [ ! -e $allprefix$tocop ]; then
				cat $eventRoot/$comparison/$tocop >> $allprefix$tocop
			else
				awk 'FNR>1' $eventRoot/$comparison/$tocop >> $allprefix$tocop	
			fi
		done

	done

done

echo "done combining simple events"

Splidar.Splicing.combineEvents_moreC.sh

echo "done combining combination of events"



for comparison in ${allComparisons[@]}; do
	
	newgeneprefix="Combined/$comparison/Genes/"
	for i in Combined/$comparison/*.xls; do
	
	numevents=`wc -l $i | cut -d" " -f1`
	#echo $i has $numevents rows
	numevents=`expr $numevents - 1` #discount header
	echo $i has $numevents events >> /dev/stderr
		
	bas=`basename $i`
	getUniqueNameFromTable.sh $i .locusName 2 > $newgeneprefix/${bas/.xls/}.genenames.txt
	numgenes=`wc -l $newgeneprefix/${bas/.xls/}.genenames.txt | cut -d" " -f1`
	echo $i has $numgenes genes >> /dev/stderr
	#echo $i $numevents $numgenes >> Combined/combineEvent.log
	done
	
done

#bash getMappingToFusedGenes.sh all.CombinedAnalysis.final.FDRm.Detectable.xls ../Combined/

echo "done gene outputing"
