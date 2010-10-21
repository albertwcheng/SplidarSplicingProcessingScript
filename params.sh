#for filtering/collapsing events (ThresholdBothJRFPooledSample is also used in SplidarAddFlag, FDR Determination
ThresholdBothJRFPooledSample=-1 #for sum over all sampels (>=) not used set to -1, use set to 1
ThresholdEitherJRFPerSample=-1 #for inJRF or exJRF >0 per sample (>=) not used set to -1, use set to 1
ThresholdSumIncExcReadsPooledSample=10 #inc+excReads in pooled sample (>=)
ThresholdIncExcReadsPerSample=10 #for inc+excReads>=10 per sample  (>=) #change from 1 -> 10 on 5/6/2010

#for SplidarAddFlag, FDR determination
ThresholdSumIncExcReadsSamplePair=10
incDetectionThreshold=5
excDetectionThreshold=5
 
filterEventCriteria=t #mmp:mininmize(min(p-value))|xmp: maximize(min(p-value))|mxp: minimize(max(p-value))|xxp: maximize(max(p-value)) |t:totalNINE
favorFlankingCobound=".flankingCoboundFlag" #no | .flankingCoboundFlag

TFThreshold=1 ####not used??
JFThreshold=1 #### (>)
FDRThreshold=0.05

#colDetectable=`colSelect.py $bgset ".TFDetectable"`
#colDetected=`colSelect.py $bgset "@TFDetected$"`
#colDetectedBoth=`colSelect.py $bgset "@TFDetectedBoth$"`
detectableColSelector=".TFDetectable"
detectedColSelector="@TFDetected$"
detectedbothColSelector="@TFDetectedBoth$"
