#!awk


BEGIN{ 
	OFS="\t"; 
	FS="\t";
	#input COLS 1 2 3 ...
	#input NAME e.g., Psi
	split(COLS,cols," ");
	split(COLNAMES,colnames," ");
	#printf("%s,%s\n",COLNAMES,COLS);

	
}

function lengthArray(arr){
	l=0;
	for(a in arr){
		l++;
	}
	return l;
}




{

	if(FNR==1){
		nCols=lengthArray(cols);
		arrayi=0
		for(i=1;i<=nCols-1;i++){
			for(j=i+1;j<=nCols;j++){
				labelname=colnames[j] "-" colnames[i] "." NAME;
				if(arrayi==0){
					printf("%s",labelname);	
				}
				else{
					printf("\t%s",labelname);
				}
				arrayi++;

			}

		}
		printf("\n");
		
	}

	else{
		arrayi=0
		for(i=1;i<=nCols-1;i++){
			for(j=i+1;j<=nCols;j++){
				diffval=$cols[j]-$cols[i];
				if(arrayi==0){
					printf("%f",diffval);	
				}
				else{
					printf("\t%f",diffval);
				}				
				arrayi++;
			}
		}		
		
		printf("\n");
	}

}

