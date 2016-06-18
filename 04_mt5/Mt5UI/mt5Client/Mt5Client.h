#pragma once

class CMt5Client
{
public:
	CMt5Client();
	~CMt5Client();
public:
	CString RequestKDataThread(LPVOID pParam);
	CString RequestCodeThread(LPVOID pParam);
	BOOL	CMt5Client::Logout(void);

private:
	char*	UnicodeToUTF_8First(CString str);
	CString Utf_8ToUnicode(char* szU8);
	BOOL	RecvAll(SOCKET sock, void *buf, int size);
};