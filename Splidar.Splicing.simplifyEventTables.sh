#!/bin/bash

if [ $# -ne 1 ]; then
	echo $0 folder
	exit 1
fi

folder=$1

cd $folder

pwd

chunk=20

jobID=0




for i in byEGString/CombinedAnalysis.final.FDRm.xls; do
	echo submit job for $i
	echo "cuta.py -F\".\" -f\".eventID,.eventType,.locusName,.chr,.strand,.inc/excBound,.UCSCGenomeBrowser,@\\.Psi,@\\.dPsi,.Defined Loci Name-_1\" $i > ${i/.xls/}.simp.xls" | bsub -o /dev/null -e /dev/null
done

#exit 0

for i in byEGString/*/CombinedAnalysis.final.FDRm.FDR*.xls; do
	if [[ $i =~ "bestpowerset" ]]; then
		continue
	fi
	
	if [[ $i =~ "intersect" ]]; then
		continue
	fi
	
	if [[ $i =~ "simp" ]]; then
		continue
	fi
	
	if [[ $i =~ "list1spec" ]]; then
		continue
	fi	
	if [[ $i =~ "list2spec" ]]; then
		continue
	fi
	
	if [[ $i =~ "union" ]]; then
		continue
	fi	
	
	if [[ $i =~ "powerSet" ]]; then
		continue
	fi		
	
	echo submit job for $i
	
	#rmrie.sh ${i/.xls/}.simp.xlx
	
	sampleName=`pyeval.py "\"$i\".split('/')[1].replace('-','^m')"` #sample name is the second component of the path
	echo sampleName is $sampleName
	
	rmrie.sh ${i/.xls/}.simp.stdout
	rmrie.sh ${i/.xls/}.simp.stderr
	echo "cuta.py -F\".\" -f\".eventID,.eventType,.locusName,.chr,.strand,.inc/excBound,.UCSCGenomeBrowser,@\\.Psi,@\\.dPsi,.Defined Loci Name-_1\" $i | splitlines.py - 1 ${i/.xls/}.simp.xls,${i/.xls/}.simp.00; colSort=\`colSelect.py ${i/.xls/}.simp.xls .$sampleName.dPsi\`; Splidar.Splicing.sortTab.sh ${i/.xls/}.simp.00 \$colSort ${i/.xls/}.simp.xls; rm ${i/.xls/}.simp.00"  | bsub -o ${i/.xls/}.simp.stdout -e ${i/.xls/}.simp.stderr
done
