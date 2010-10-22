#!/bin/bash

for event in RI SE MXE A5SS A3SS  A3UTR AFE  ALE; do
	if [ -e $event ]; then
		cd $event
		echo cleaning event $event
		rm -Rf byEGString *.00 *.highlyRedundant *.log *.xls scripts
		rm -Rf */*.00 
		rm -Rf */*.merged.* 
		rm -Rf */*.header.txt
		cd ..
	fi
done

for splitEvent in A5SS A3SS AFE ALE; do
	if [ -e $splitEvent ]; then
		rm -Rf $splitEvent
	fi
done
