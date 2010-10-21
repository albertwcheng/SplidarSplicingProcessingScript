#!/bin/bash

#separate AFE and ALE
if [ $# -lt 1 ]; then
echo todo.sh genome [hg18 , mm9]
exit
fi

genome=$1

if [ 1 -eq 0 ]; then

cd ..

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


#####

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



fi


cd ..


#####
echo "done reorganizing"

for event in  A3UTR   ; do #SE MXE RI  SE MXE RI_TT A5SS A3SS   A3UTR SE  #SE MXE RI A5SS A3SS AFE ALE  A5SS A3SS AFE ALE SE MXE RI A5SS A3SS AFE ALE
	echo "merging event $event"
	cd $event
	cp -R ../SplidarProcessingScript/scripts .
	cd scripts
	bash mergeSplidarOutput.sh $genome $event	
	cd ..
	cd ..
done
		
