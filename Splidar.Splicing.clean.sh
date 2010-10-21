
cd ..

for event in RI SE MXE A5SS A3SS  A3UTR AFE  ALE; do
	cd $event
	echo cleaning event $event
	rm -R byEGString *.00 *.highlyRedundant *.log *.xls scripts
	cd ..
done
