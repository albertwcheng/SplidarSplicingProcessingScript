#!/bin/bash

:<<'COMMENT'

colStat.py BAT_D5_vs_BAT_D0.SE.bf5.miso_bf.splidarEvents.tab 
[:::::			R 1			:::::]
Index			Excel			Field
-----			-----			-----
1			A			eventIDString
2			B			eventType
3			C			eventID
4			D			locusName
5			E			chr
6			F			strand
7			G			inc/excBound
8			H			UCSCGenomeBrowser
9			I			sample1_posterior_mean
10			J			sample1_ci_low
11			K			sample1_ci_high
12			L			sample2_posterior_mean
13			M			sample2_ci_low
14			N			sample2_ci_high
15			O			diff
16			P			bayes_factor

COMMENT

