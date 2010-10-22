#include <string>
#include <iostream>
#include <apop.h>
#include <fstream>
#include <vector>
#include <map>

#include "StringUtil.h"
using namespace std;



double ftest(double n1, double n2, double n3, double n4)
{
  double p;
  double data[4];
  data[0]=n1; data[1]=n2;data[2]=n3;data[3]=n4;
  apop_data *testdata = apop_line_to_data(data,0,2,2), *res;
  
  /* execute fisher test */
  res = apop_test_fisher_exact(testdata);
  //p = gsl_matrix_get(res->matrix,1,0);
  p = apop_data_get(res,1,-1);

  /* free allocated data structs */
  apop_data_free(res);
  apop_data_free(testdata);

  return p;
}


#define BUFFERSIZE 1024*1024*10

void ftestPrint(const char* filename,int col1,int col2,int col3,int col4,int startRow)
{
	ifstream fin(filename);
	char *buffer=new char[BUFFERSIZE];
	
	int lino=0;
	while(!fin.eof())
	{
		
		buffer[0]='\0';
		fin.getline(buffer,BUFFERSIZE);
		
		if(buffer[0]=='\0')
			break;
		
		lino++;
		if(lino<startRow)
			continue;
		
		vector<string> spliton;
		StringUtil::split(buffer,string("\t"),spliton,true);
		
		double d1=StringUtil::atof(spliton[col1-1]);
		double d2=StringUtil::atof(spliton[col2-1]);
		double d3=StringUtil::atof(spliton[col3-1]);
		double d4=StringUtil::atof(spliton[col4-1]);
		if (int(d1)+int(d2)+int(d3)+int(d4)==0)
			cout<<"nan"<<endl;
		else
			cout<<ftest(d1,d2,d3,d4)<<endl;
	}
	delete buffer;
	fin.close();
}

void ftest_testftest(double n1, double n2, double n3, double n4)
{
  double p;
  double data[4];
  data[0]=n1; data[1]=n2;data[2]=n3;data[3]=n4;
  apop_data *testdata = apop_line_to_data(data,0,2,2), *res;
  
  /* execute fisher test */
  res = apop_test_fisher_exact(testdata);
  //p = gsl_matrix_get(res->matrix,1,0);
  
  
 // for(int i=0;i<res->vector->size;i++)
 // 	cerr<<"res->vector["<<i<<"]"<<"="<<apop_data_get(res,i,-1)<<endl;
  apop_data_show(res); 

  /* free allocated data structs */
  apop_data_free(res);
  apop_data_free(testdata);

  
}

int main(int argc,const char*argv[])
{
	//ftest_testftest(372,13,24,268);
	
	//return 1;
	if(argc<7)
	{
		cerr<<"Usage:"<<argv[0]<<" filename col1[1] col2[1] col3[1] col4[1] startRow[1]"<<endl;
		return 0;
	}
	ftestPrint(argv[1],StringUtil::atoi(argv[2]),StringUtil::atoi(argv[3]),StringUtil::atoi(argv[4]),StringUtil::atoi(argv[5]),StringUtil::atoi(argv[6]));
	return EXIT_SUCCESS;
}

