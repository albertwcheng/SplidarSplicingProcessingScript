#!/bin/bash



scriptDir=$1
rootDir=$2
sample=$3
TAB=`echo -e "\t"`

echo "merging splidar sequence from sample $sample" > /dev/stderr

cd $rootDir

cd $sample

eventKeyStart=`colSelect.py $scriptDir/Splidar.Splicing.headerGeneric.txt .eventType`
eventKeyStart=`expr $eventKeyStart - 1`
eventKeyEnd=`colSelect.py $scriptDir/Splidar.Splicing.headerGeneric.txt .UCSCGenomeBrowser`
eventKeyEnd=`expr $eventKeyEnd - 1`

cat $sample.*.seq.xls > ../seq.headless.00
awk '{print FNR}' ../seq.headless.00 > ../eventID.00

cut -d"$TAB" -f$eventKeyStart-$eventKeyEnd ../seq.headless.00 > ../eventKey.00

paste ../eventID.00 ../seq.headless.00 > ../seq.merged.headless.wEID.00


sort -k1,1 ../seq.merged.headless.wEID.00 > ../seq.merged.highlyRedundant

cat $scriptDir/Splidar.Splicing.seqHeader.txt ../seq.merged.highlyRedundant > ../seq.merged.xls

cd $scriptDir



