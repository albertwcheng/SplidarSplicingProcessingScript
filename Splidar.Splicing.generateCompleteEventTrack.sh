#!/bin/bash

myPath=`absdirname.py $0`
scriptDir=$myPath
inPath=`checkInPath.sh Splidar.Splicing.mergeSplidarOutput.sh`

if [[ $inPath == 0 ]]; then #not in path
	echo "not in path. add path"
	export PATH=${PATH}:$scriptDir
	
fi


rm allEvents.complete.ebed

for eventType in SE MXE A3SS A5SS A3UTR AFE ALE MXE RI; do
echo "making bed file for $eventType"
Splidar.Splicing.EventBEDMaker.py --track-name $eventType --colors "255,0,0_0,0,255" "$eventType/seq.merged.xls" .eventType,.locusName,.eventID .chr .strand ".inc/excBound" > "$eventType/$eventType.complete.ebed" 
cat "$eventType/$eventType.complete.ebed"  >> allEvents.complete.ebed
done

