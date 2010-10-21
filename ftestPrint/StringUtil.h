#ifndef STRINGUTIL_H_
#define STRINGUTIL_H_



#include <vector>
#include <string>
#include <map>
#include <ctype.h>
using namespace std;

#define BUFFER_SIZE 1025

#define THRESHOLD_TRIM_BUFFER_TIME 10
#define THRESHOLD_TRIM_BUFFER_COMP 10240


template<class T>
class buffer
{
private:
	T*data;
	int size;
	int smallerRequested;
public:
	inline T* buf()
	{
		return data;
	}
	int capacity()
	{
		return size;
	}
	buffer(int _size=BUFFER_SIZE):size(0),data(NULL)
	{
		buf(_size);
	}
	T* realloc(int _size)
	{
		if(data)
		{
			delete[] data;
		}

		data=new T[_size];
		size=_size;
		smallerRequested=0;

		return data;
	}
	T& operator[] (int i){
		return data[i];
	}

	T* buf(int _size)
	{
		//cerr<<"buffer for "<<_size<<endl;
		if(_size>size || data==NULL)
		{

			realloc(_size);

		}
		else if (size>_size+THRESHOLD_TRIM_BUFFER_COMP)
		{
			smallerRequested++;
			if(smallerRequested>=THRESHOLD_TRIM_BUFFER_TIME)
			{
				realloc(_size);

			}
		}
		return data;

	}
	~buffer()
	{
		delete[] data;
	}
};

template<class T1,class T2>
class KeyPair
{
public:
	T1 k1;
	T2 k2;
	inline KeyPair():k1(0),k2(0){}
	KeyPair(T1 _k1,T2 _k2): k1(_k1), k2(_k2) {
	}

	inline bool operator <(const KeyPair<T1,T2>& obj) const
	{
		if(this->k1==obj.k1)
		{
			return (this->k2<obj.k2);
		}

		return this->k1<obj.k1;

	}

	inline bool operator !=(const KeyPair<T1,T2>& obj) const
	{
		return !((*this)==obj);
	}

	inline bool operator >=(const KeyPair<T1,T2>& obj) const
	{
		return !((*this)<obj);
		//return (*this)>obj || (*this)==obj;
	}

	inline bool operator <=(const KeyPair<T1,T2>& obj) const
	{
		return !((*this)>obj);
		//return (*this)<obj || (*this)==obj;
	}

	bool operator ==(const KeyPair<T1,T2>& obj) const
	{
		return this->k1==obj.k1 && this->k2==obj.k2;
	}

	bool operator >(const KeyPair<T1,T2>& obj) const
	{
		if(this->k1==obj.k1)
		{
			return (this->k2>obj.k2);
		}

		return this->k1>obj.k1;

	}
};

template<class T1,class T2>
ostream& operator << ( ostream&os,const KeyPair<T1,T2>&k)
{
	os<<k.k1<<"\t"<<k.k2;
	return os;
}

class StringUtil
{
public:

	inline static string str(int d)
	{
		return str(d,"%d");
	}

	inline static string str(double d)
	{
		return str(d,"%f");
	}

	inline static string str(double d,int precision)
	{
		return str(d,string("%.")+str(precision)+"f");
	}

	template<class T>
	inline static string str(T d,string format)
	{
		return str(d,format.c_str());
	}

	template<class T>
	inline static string str(T d,const char* format)
	{
		char buffer[100];
		sprintf(buffer,format,d);
		return string(buffer);
	}


	inline static int atoi(const char* s)
	{
		return ::atoi(s);
	}


	inline static double atof(const char *s)
	{
		return ::atof(s);
	}
	inline static string formArrayString( vector<string>& arr,string sep="|")
	{
		vector<string>::iterator i=arr.begin();
		if(i==arr.end()) return "";
		string result=(*i);
		for(;i!=arr.end();i++)
		{
			result+=sep+(*i);
		}
		return result;
	}
	inline static string formKeyValueString( map<string,string>& _map,string sep="|",string equ="=")
	{

		map<string,string>::iterator i=_map.begin();
		if(i==_map.end())
			return "";
		string result=(*i).first+equ+(*i).second;
		i++;
		for(;i!=_map.end();i++)
		{
			result+=sep+(*i).first+equ+(*i).second;
		}

		return result;
	}

	 inline static int atoi(string s)
	{
		return atoi(s.c_str());
	}


	inline static double atof(string s)
	{
		return atof(s.c_str());
	}
	inline static string toUpper(const string& str)
	{
		int len=str.length();
		char *tmp=new char[len+1];
		register const char*cur=str.c_str();
		register const char*terminal=cur+len;
		register char *tmp2=tmp;

		for(;cur<terminal;cur++,tmp2++)
		{
			*tmp2=toupper(*cur);
		}

		tmp[len]='\0';
		string tstr=string(tmp);
		delete[] tmp;
		return tstr;
	}

	inline static string toLower(const string&str)
	{
		int len=str.length();
		char *tmp=new char[len+1];
		register const char*cur=str.c_str();
		register const char*terminal=cur+len;
		register char *tmp2=tmp;

		for(;cur<terminal;cur++,tmp2++)
		{
			*tmp2=tolower(*cur);
		}

		tmp[len]='\0';
		string tstr=string(tmp);
		delete[] tmp;
		return tstr;
	}
	inline static string stripAll(string haystack,string remove)
	{
		const char * str=haystack.c_str();
		const char * removestr=remove.c_str();
		int rlen=remove.length();
		int len=haystack.length();

		int k=0;

		buffer<char> buff(len+1);
		char *bstr=buff.buf();
		for(int i=0;i<len;i++)
		{
			bool exclude=false;
			for(int j=0;j<rlen;j++)
			{
				if(str[i]==removestr[j])
				{
					exclude=true;

				}
			}

			if(!exclude)
				bstr[k++]=str[i];
		}

		bstr[k]='\0';
		return string(bstr);
	}


	
	static void splitInt2(string haystack,string sep,vector<int>& v,bool clear=true)
	{
		if(clear)
			v.clear();
		
		
		vector<string> spliton;
		split(haystack,sep,spliton);
		//v.resize(spliton.size());
		
		//int j=0;
		for(vector<string>::iterator i=spliton.begin();i!=spliton.end();i++)
			v.push_back(StringUtil::atoi(*i));
	
		
	}

	static vector<int> splitInt(string haystack,string sep="\t")
	{
		/*vector<string> spliton;
		split(haystack,sep,spliton);
		vector<int> v(spliton.size());
		int j=0;
		for(vector<string>::iterator i=spliton.begin();i!=spliton.end();i++)
			v[j++]=StringUtil::atoi(*i);*/
		
		vector<int> v;
		
		StringUtil::splitInt2(haystack,sep,v,true);

		return v;
	}
	
	inline static vector<string>& split(const string haystack,const string& needle,vector<string>& vec,bool clear=true)
	{

		int hslen=haystack.length();
		int needlen=needle.length();
		const char *shaystack=haystack.c_str();
		char *hay=new char[hslen+1];
		strcpy(hay,shaystack);
		const char *sneedle=needle.c_str();

		if(clear)
			vec.clear();

		int start=0;


		for(int i=0;i<hslen;i++)
		{
			char c=hay[i];
			bool found=false;
			for(int j=0;j<needlen;j++)
			{
				if (sneedle[j]==c)
					found=true;
			}
			if(found)
			{
				hay[i]='\0';
				vec.push_back((hay+start));
				hay[i]=' ';
				start=i+1;
			}
		}

		if(start<hslen)
		{
			vec.push_back( (shaystack+start));
		}


		delete[] hay;
		return vec;
	}
};

#endif /*STRINGUTIL_H_*/
