#!/bin/bash

#separate AFE and ALE
if [ $# -lt 1 ]; then
	echo todo.sh paramFile
exit
fi




####set path

myPath=`absdirname.py $0`
scriptDir=$myPath
inPath=`checkInPath.sh Splidar.Splicing.mergeSplidarOutput.sh`

if [[ $inPath == 0 ]]; then #not in path
	echo "not in path. add path"
	export PATH=${PATH}:$scriptDir
	
fi

inPath=`checkInPath.sh ftestPrint`

if [[ $inPath == 0 ]]; then #not in path
	echo "not in path. add path"
	export PATH=${PATH}:$scriptDir/ftestPrint
	
fi

paramFile=$1
paramFile=`abspath.py $paramFile`  #get the abs path of param file such that it can be used even when pwd is not the same

if [ ! -e AFE ] || [ ! -e ALE ]; then
if [ -e ATE ]; then  

echo "splitting ATE into AFE and ALE"
mkdir ALE
mkdir AFE

cd ATE

cp manifest.txt ../AFE
cp manifest.txt ../ALE


for sample in *; do
	if [ -d $sample ]; then
		cd $sample
		
		for subevent in AFE ALE; do

			
			mkdir ../../$subevent/$sample			
			for fil in *.exinc.xls; do
				awk -v subevent=$subevent '$1==subevent' $fil > ../../$subevent/$sample/$fil
			done
			
			seqfiles=$(ls *.exinc.seq.xls 2> /dev/null | wc -l)

			if [ $seqfiles != "0" ]; then
				for fil in *.exinc.seq.xls; do
					awk -v subevent=$subevent '$1==subevent' $fil >	../../$subevent/$sample/$fil
				done
			fi
		done

		cd ..
	fi
done

cd ..

fi
fi

#####

if [ ! -e A5SS ] || [ ! -e A3SS ]; then
if [ -e A53SS ]; then  


echo "splitting A53SS into A5SS and A3SS"
mkdir A5SS
mkdir A3SS

cd A53SS

cp manifest.txt ../A5SS
cp manifest.txt ../A3SS


for sample in *; do
	if [ -d $sample ]; then
		cd $sample
		
		for subevent in A5SS A3SS; do

			
			mkdir ../../$subevent/$sample			
			for fil in *.exinc.xls; do
				awk -v subevent=$subevent '$1==subevent' $fil > ../../$subevent/$sample/$fil
			done
			
			seqfiles=$(ls *.exinc.seq.xls 2> /dev/null | wc -l)

			if [ $seqfiles != "0" ]; then
				for fil in *.exinc.seq.xls; do
					awk -v subevent=$subevent '$1==subevent' $fil >	../../$subevent/$sample/$fil
				done
			fi
		done

		cd ..
	fi
done





cd ..

fi
fi

#####
echo "done reorganizing"

for event in SE MXE RI A5SS A3SS  AFE ALE  A3UTR   ; do #SE MXE RI  SE MXE RI_TT A5SS A3SS   A3UTR SE  #SE MXE RI A5SS A3SS AFE ALE  A5SS A3SS AFE ALE SE MXE RI A5SS A3SS AFE ALE
	echo "merging event $event"
	#cd $event
	#cp -R ../SplidarProcessingScript/scripts .
	#cd scripts
	Splidar.Splicing.mergeSplidarOutput.sh $paramFile $event	
	#cd ..
	#cd ..
done
		
