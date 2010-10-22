#!/bin/bash

#
# Version 2010-3-16
#
#


#cd ../byEGString

if [ $# -lt 7 ]; then
	echo Usage: $0 FDRColSelector FDRThreshold dPsiColSelector dPsiThresholdLower dPsiThresholdUpper bgset scriptDir
	exit
fi

FDRColSelector=$1
FDRThreshold=$2
dPsiColSelector=$3
dPsiThresholdLower=$4
dPsiThresholdUpper=$5
bgSet=$6
scriptPath=$7

#bgSet="CombinedAnalysis.final.FDRm.xls"

#colStat.py $bgSet




echo FDRColSelector=$FDRColSelector `head -n 1 $bgSet | cut -f$FDRColSelector`
echo dPsiColSelector=$dPsiColSelector `head -n 1 $bgSet | cut -f$dPsiColSelector`
echo FDRThreshold=$FDRThreshold


if [ $dPsiThresholdUpper == 0.0 ]; then
	fgSet=${bgSet/.xls/}.FDR${FDRThreshold}.xls
	awk -v FDRColSelector=$FDRColSelector -v dPsiColSelector=$dPsiColSelector -v FDRThreshold=$FDRThreshold  'BEGIN{FS="\t";OFS="\t";}(FNR==1 || (FNR>1 && $FDRColSelector<FDRThreshold ))' $bgSet > $fgSet
else
	echo dPsiThresholdLower=$dPsiThresholdLower
	echo dPsiThresholdUpper=$dPsiThresholdUpper
	fgSet=${bgSet/.xls/}.FDR${FDRThreshold}_dPsi$dPsiThresholdLower$dPsiThresholdUpper.xls
	awk -v FDRColSelector=$FDRColSelector -v dPsiColSelector=$dPsiColSelector -v FDRThreshold=$FDRThreshold -v dPsiThresholdLower=$dPsiThresholdLower -v dPsiThresholdUpper=$dPsiThresholdUpper 'BEGIN{FS="\t";OFS="\t";}(FNR==1 || (FNR>1 && $FDRColSelector<FDRThreshold && ($dPsiColSelector<=dPsiThresholdLower || $dPsiColSelector>=dPsiThresholdUpper)))' $bgSet > $fgSet
fi



echo "getting event counts. Remember to minus one to discount header"
wc -l $fgSet 



powersetpref=${fgSet/.xls/powerSet}  #CombinedAnalysis.final.FDRm.FDR0.05_dPsi-0.40.4powerSet


Splidar.Splicing.findPowerSet.py --iterate-median-B4 100 $fgSet $bgSet $powersetpref 2> ${fgSet/.xls/}_powerset.log

source ${fgSet/.xls/}_powerset.log

bestpowerset=${fgSet/.xls/}_bestpowerset.xls
ibestpset=${#fps_pset[@]}
bestpowersetorig=${fps_pset[$ibestpset]}

echo setting the $ibestpset th powerset [ $bestpowersetorig ] as the best set by median B4 criteria

cp $bestpowersetorig $bestpowerset #CombinedAnalysis.final.FDRm.FDR0.05_dPsi-0.40.4_bestpowerset.xls
#compareLists.py --headerFrom1To 1 --outprefix a --outsuffix .00 l1 l2v

compareLists.py --headerFrom1To 1 --outprefix ${fgSet/.xls/}bps --outsuffix .xls $fgSet $bestpowerset

#now we have CombinedAnalysis.final.FDRm.FDR0.05_dPsi-0.40.4bps_intersect.xls _list1spec.xls (which is the fgset specific) _list2spec.xls (which is the powerset specific) 


#make union of sigset and powerset
awk '(FNR>1)' ${fgSet/.xls/}bps_list1spec.xls > ${fgSet/.xls/}bps_list1spec.headless.00
cat $bestpowerset ${fgSet/.xls/}bps_list1spec.headless.00 > ${fgSet/.xls/}bps_union.xls








cd $scriptPath

#echo "power set generated. getting event count. Remember to minus one to discount header"
#wc -l $powerset
