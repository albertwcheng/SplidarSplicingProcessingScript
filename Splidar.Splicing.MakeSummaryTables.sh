#!/bin/bash

if [ $# -lt 3 ];then
	echo $0 columnsSpec eventsSpec outputDir
	exit
fi

columnsSpec=$1
eventsSpec=$2
outputDir=$3

mkdir.py $outputDir

