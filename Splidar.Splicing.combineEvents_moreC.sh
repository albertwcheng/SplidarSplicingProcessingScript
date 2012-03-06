cd Combined/

for subF in *; do

if [ -e $subF/SE.CombinedAnalysis.final.FDRm.Detectable.xls ]; then

cd $subF

tocopy[1]=CombinedAnalysis.final.FDRm.Detectable.xls
tocopy[2]=CombinedAnalysis.final.FDRm.DetectedBoth.xls
tocopy[3]=CombinedAnalysis.final.FDRm.FDR0.05.xls
tocopy[4]=CombinedAnalysis.final.FDRm.FDR0.05_dPsi-0.10.1.xls
tocopy[5]=CombinedAnalysis.final.FDRm.FDR0.05_dPsi-0.30.3.xls
tocopy[6]=CombinedAnalysis.final.FDRm.FDR0.05_dPsi-0.10.1bps_union.xls
tocopy[7]=CombinedAnalysis.final.FDRm.FDR0.05_dPsi-0.30.3bps_union.xls
tocopy[8]=CombinedAnalysis.final.FDRm.FDR0.05bps_union.xls

eventCombinations[1]="SE+MXE"
eventCombinations[2]="SE+MXE+A5SS+A3SS+ALE"
eventCombinations[3]="SE+MXE+A5SS+A3SS+ALE+RI"
eventCombinations[4]="SE+MXE+A5SS+A3SS+ALE+RI+A3UTR"

for eventCombination in ${eventCombinations[@]}; do
	saveIFS=$IFS
	IFS=`echo "+"`
	declare -a eventArray=( $eventCombination )
	IFS=$saveIFS
	numEvents=${#eventArray[@]}
	echo $eventCombination has $numEvents events
	for((i=0;i<$numEvents;i++));do
		thisEvent=${eventArray[$i]}
		echo event[$i]=$thisEvent
		for tc in ${tocopy[@]}; do
			splitlines.py $thisEvent.$tc 1 $tc.head.00,$eventCombination.$i.$tc.00
		done
	done

	for tc in ${tocopy[@]}; do
		ls $eventCombination.*.$tc.00 | tr "\n" ":"
		echo ""
		cat $tc.head.00 $eventCombination.*.$tc.00 > $eventCombination.$tc
	done
done

rm *.00

cd ..

fi



done
