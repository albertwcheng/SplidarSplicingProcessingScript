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

if [ -e A53SS ]; then
	for splitEvent in A5SS A3SS; do
		if [ -e $splitEvent ]; then
			rm -Rf $splitEvent
		fi
	done
fi

if [ -e ATE ]; then
	for splitEvent in AFE ALE; do
		if [ -e $splitEvent ]; then
			rm -Rf $splitEvent
		fi
	done
fi