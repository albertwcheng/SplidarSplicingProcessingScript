#!/bin/bash

if [ $# -lt 3 ]; then
	echo $0 infile col outfile
	exit 1
fi

infile=$1
col=$2
outfile=$3

sort -k$col -t$'\t' -g -r $infile >> $outfile