#pragma once
//#include "windows.h"
#include <string>
#include "Logger.h"
#include <ctime>
#include <vector>
#include "json/json.h"
#include <fstream>
#include <sys/time.h>

class Util {
public:
    static int getTime(timespec * time){
        clock_gettime(CLOCK_MONOTONIC,time);
    }
    static Json::Value loadJson(string file){
        Json::Reader reader ;
        Json::Value root ;
        ifstream in(file.data(),ios::binary);
        if(!in.is_open()){
            cout << "can not open file " << file << endl ;
            exit(1);
        }
        reader.parse(in,root);
        in.close();
        return root;
    }
    static void split(const string& s, vector<string>& tokens, const string& delimiters = " ")
    {
        string::size_type lastPos = s.find_first_not_of(delimiters, 0);
        string::size_type pos = s.find_first_of(delimiters, lastPos);
        while (string::npos != pos || string::npos != lastPos) {
            tokens.push_back(s.substr(lastPos, pos - lastPos));//use emplace_back after C++11
            lastPos = s.find_first_not_of(delimiters, pos);
            pos = s.find_first_of(delimiters, lastPos);
        }
    }

    static double delaynsec(timespec * begin, timespec *end)
    {
        return (end->tv_sec * 1000000000 + end->tv_nsec ) -
               (begin->tv_sec * 1000000000 + begin->tv_nsec);
    }
    static void toCString(const std::vector<std::string>& source, char** destination)
    {
        // 注意释放内存
        for (int n = 0; n < static_cast<int>(source.size()); n++)
        {
            destination[n] = new char[32];
            destination[n][31] = '\0';
            strncpy(destination[n], source[n].c_str(), 31);
        }
        //destination[source.size()] = NULL;
    }



    /*static LPCWSTR stringToLPCWSTR(std::string orig)
    {
        size_t origsize = orig.length() + 1;
        const size_t newsize = 100;
        size_t convertedChars = 0;
        wchar_t* wcstring = (wchar_t*)malloc(sizeof(wchar_t) * (orig.length() - 1));
        mbstowcs_s(&convertedChars, wcstring, origsize, orig.c_str(), _TRUNCATE);

        return wcstring;
    }

    static std::string UnicodeToUtf8(const std::wstring& strUnicode)
    {
        int len = WideCharToMultiByte(CP_UTF8, 0, strUnicode.c_str(), -1, NULL, 0, NULL, NULL);
        if (len == 0)
        {
            return "";
        }

        char* pRes = new char[len];
        if (pRes == NULL)
        {
            return "";
        }

        WideCharToMultiByte(CP_UTF8, 0, strUnicode.c_str(), -1, pRes, len, NULL, NULL);
        pRes[len - 1] = '\0';
        std::string result = pRes;
        delete[] pRes;

        return result;
    }
    static std::wstring Utf8ToUnicode(const std::string& strUTF8)
    {
        int len = MultiByteToWideChar(CP_UTF8, 0, strUTF8.c_str(), -1, NULL, 0);
        if (len == 0)
        {
            return L"";
        }

        wchar_t* pRes = new wchar_t[len];
        if (pRes == NULL)
        {
            return L"";
        }

        MultiByteToWideChar(CP_UTF8, 0, strUTF8.c_str(), -1, pRes, len);
        pRes[len - 1] = L'\0';
        std::wstring result = pRes;
        delete[] pRes;

        return result;
    }


    static std::wstring StringToWString(const std::string& str)
    {
        int len = MultiByteToWideChar(CP_ACP, 0, str.c_str(), -1, NULL, 0);
        if (len == 0)
        {
            return L"";
        }

        wchar_t* pRes = new wchar_t[len];
        if (pRes == NULL)
        {
            return L"";
        }

        MultiByteToWideChar(CP_ACP, 0, str.c_str(), -1, pRes, len);
        pRes[len - 1] = L'\0';
        std::wstring result = pRes;
        delete[] pRes;

        return result;
    }

    static std::string WStringToString(const std::wstring& wstr)
    {
        int len = WideCharToMultiByte(CP_ACP, 0, wstr.c_str(), -1, NULL, 0, NULL, NULL);
        if (len == 0)
        {
            return "";
        }

        char* pRes = new char[len];
        if (pRes == NULL)
        {
            return "";
        }

        WideCharToMultiByte(CP_ACP, 0, wstr.c_str(), -1, pRes, len, NULL, NULL);
        pRes[len - 1] = '\0';
        std::string result = pRes;
        delete[] pRes;

        return result;

    }*/

};
