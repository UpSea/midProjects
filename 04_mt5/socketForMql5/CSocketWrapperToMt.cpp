#include "CSocketWrapperToMt.h"
CSocketWrapperToMt::CSocketWrapperToMt()
{
}
CSocketWrapperToMt::~CSocketWrapperToMt()
{
}
ULONG CSocketWrapperToMt::my_rand()
{
	return (ULONG)__rdtsc();
}
BOOL RecvAll(SOCKET sock, void *buf, int size)
{
	int err;
	int index = 0;
	while (size != 0)
	{
		err = recv(sock, (char*)buf + index, size, 0);
		if (err == SOCKET_ERROR) break;
		else if (err == 0) break;
		size -= err;
		index += err;
	}
	return size == 0;
}

BOOL SendAll(SOCKET sock, void *buf, int size)
{
	int err;
	int index = 0;
	while (size != 0)
	{
		if (size > 4096)
		{
			err = send(sock, (char*)buf + index, 4096, 0);
		}
		else
		{
			err = send(sock, (char*)buf + index, size, 0);
		}
		if (err == SOCKET_ERROR) break;
		else if (err == 0) break;
		size -= err;
		index += err;
	}
	return size == 0;
}

//+------------------------------------------------------------------+
//|		Host2Ip				                                        |
//+------------------------------------------------------------------+
ULONG CSocketWrapperToMt::Host2Ip(char * host)
{
	struct hostent * p;
	ULONG ret;
	p = gethostbyname(host);
	if (p) ret = *(ULONG*)(p->h_addr);
	else ret = INADDR_NONE;
	return ret;
}

//+------------------------------------------------------------------+
//|		ConnectToServer												|
//+------------------------------------------------------------------+
ULONG CSocketWrapperToMt::ConnectToServer(char * host, USHORT port)
{
	struct sockaddr_in addr;
	BOOL bOptVal = TRUE;
	int bOptLen = sizeof(BOOL);

	ULONG ip;
	SOCKET sock = INVALID_SOCKET;

	ip = Host2Ip(host);
	if (ip != INADDR_NONE)
	{
		addr.sin_addr.S_un.S_addr = ip;
		addr.sin_port = htons(port);

		if (addr.sin_addr.S_un.S_addr != INADDR_NONE)
		{
			addr.sin_family = AF_INET;
			sock = (ULONG)socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);//IPPROTO_TCP

			if (sock != INVALID_SOCKET)
			{
				if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)))
				{
					closesocket(sock);
					sock = INVALID_SOCKET;
				}
			}
		}
	}

	return (ULONG)sock;
}
ULONG CSocketWrapperToMt::ListenToClient(char * host, USHORT port)
{
	//struct sockaddr_in addr;
	BOOL bOptVal = TRUE;
	int bOptLen = sizeof(BOOL);

	ULONG ip;
	SOCKET sock = INVALID_SOCKET;

	ip = Host2Ip(host);
	if (ip != INADDR_NONE)
	{
		m_SocketServAddr.sin_addr.S_un.S_addr = ip;
		m_SocketServAddr.sin_port = htons(port);

		if (m_SocketServAddr.sin_addr.S_un.S_addr != INADDR_NONE)
		{
			m_SocketServAddr.sin_family = AF_INET;
			sock = (ULONG)socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);//IPPROTO_TCP

			if (sock != INVALID_SOCKET)
			{
				if (bind(sock, (sockaddr*)&m_SocketServAddr, sizeof(m_SocketServAddr)))
				{
					DWORD dwErr = GetLastError();
					//TRACE("�󶨴���");
					closesocket(sock);
					sock = INVALID_SOCKET;
				}
				else
				{
					listen(sock, 5);
				}
				//if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)))
				//{
				//}
			}
		}
	}

	return (ULONG)sock;
}

ULONG CSocketWrapperToMt::SocketConnectToServer(PSOCKET_MT client, wchar_t * wc_host, USHORT port)
{
	/*mid
		�����͑����B������������socket���B��
		���ɹ��B�ӣ��t���سɹ� ERROR_SUCCESS
		���B��ʧ�����t���؟oЧ ERROR_INVALID_HANDLE
	*/
	ULONG ret = ERROR_INVALID_HANDLE;

	char *host = new char[wcslen(wc_host) + 1];
	wcstombs(host, wc_host, wcslen(wc_host) + 1);

	client->status = SOCKET_STATUS_CLIENT_DISCONNECTED;
	client->sequence = (USHORT)my_rand();
	client->sock = ConnectToServer(host, port);

	if (client->sock == INVALID_SOCKET)
	{
		closesocket(client->sock);
	}
	else
	{
		client->status = SOCKET_STATUS_CLIENT_CONNECTED;
		ret = ERROR_SUCCESS;
	}
	delete(host);

	return(ret);
}
ULONG CSocketWrapperToMt::SocketListenToClient(PSOCKET_MT pServer, wchar_t * wc_host, USHORT port)
{
	/*mid 
		������ ������socket������socket
		�����Ѵ��� IP:PORT ���ݡ�acceptʱʹ��
	
	*/
	ULONG ret = ERROR_INVALID_HANDLE;

	char *host = new char[wcslen(wc_host) + 1];
	wcstombs(host, wc_host, wcslen(wc_host) + 1);

	pServer->status = SOCKET_STATUS_SERVER_NOTLISTENING;
	pServer->sequence = (USHORT)my_rand();
	pServer->sock = ListenToClient(host, port);

	if (pServer->sock == INVALID_SOCKET)
	{
		closesocket(pServer->sock);
	}
	else
	{
		pServer->status = SOCKET_STATUS_SERVER_LISTENING;
		ret = ERROR_SUCCESS;
	}
	//m_SocketServMt = *pServer;
	delete(host);
	return(ret);
}
ULONG CSocketWrapperToMt::SocketAcceptClient(PSOCKET_MT pSocketServerListening, PSOCKET_MT pSocketAccepted)
{
	/*mid 
		������ ������socket������socket
	
	*/
	//pMt5->m_SocketRecv[nRecvSocketIndex] = accept(pMt5->m_SocketAccept, (sockaddr*)&(pMt5->m_SocketServAddr), &(pMt5->m_nSocketServAddrSize));
	int iSizeOfSocketServAddr = sizeof(m_SocketServAddr);
	//SOCKET socketAccepted = accept((SOCKET)pServer->sock, (sockaddr*)&m_SocketServAddr, &(iSizeOfSocketServAddr));
	pSocketAccepted->sock = accept((SOCKET)pSocketServerListening->sock, (sockaddr*)&m_SocketServAddr, &(iSizeOfSocketServAddr));
	if (pSocketAccepted->sock == INVALID_SOCKET)
	{
		return ERROR_INVALID_HANDLE;
	}
	else
	{
		return ERROR_SUCCESS;
	}
	return 0;
}
void	CSocketWrapperToMt::SocketClose(PSOCKET_MT client)
{
	ULONG ret = ERROR_INVALID_HANDLE;

	if (client->status == SOCKET_STATUS_SERVER_LISTENING)
	{
		closesocket(client->sock);
		client->status = SOCKET_STATUS_CLIENT_DISCONNECTED;
		ret = GetLastError();
		if (ret != 0)
		{
			wchar_t *str = SocketErrorString(ret);
			MessageBox(NULL, str, L"Err", NULL);
		}
	}
	else
	{
		wchar_t status[16];
		_itow(client->status, status, 10);

		MessageBox(NULL, status, L"Err", NULL);
	}
}
wchar_t * CSocketWrapperToMt::SocketErrorString(int error_code)
{
	wchar_t buffer[255] = { 0 };
	if (FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM, 0, error_code, LANG_NEUTRAL, buffer, 255, 0)>0)
	{
		for (size_t i = 0; i<wcslen(buffer); i++)
			if (buffer[i]>0 && buffer[i]<32) buffer[i] = 32;
	}
	else
	{
		wchar_t strerr[16];
		_itow(error_code, strerr, 10);
		wcscpy(&buffer[0], L"Error ");
		wcscpy(&buffer[6], strerr);
	}
	return(&buffer[0]);
}
ULONG	CSocketWrapperToMt::SocketSend(PSOCKET_MT client, void * pData, int nBytesToSend, int *pnBytesSent, int nFlag)
{
	//mid Ӧ��ʹ�õ�һ�ַ�ʽ�����������ʷ�����շ�����
	
	if (FALSE)
	{
		ULONG ret = ERROR_INVALID_HANDLE;
		char *pCharData = (char *)pData;

		*pnBytesSent = send(client->sock, pCharData, nBytesToSend, nFlag);
		if (SendAll(client->sock, pCharData, nBytesToSend))
		{
			*pnBytesSent = nBytesToSend;
			ret = ERROR_SUCCESS;
		}
		else
		{
			{	//mid ���Ք�����С��һ�£�ݔ����ֵ
				wchar_t strToSend[25];
				wchar_t strSent[25];
				_itow(nBytesToSend, strToSend, 10);
				_itow(*pnBytesSent, strSent, 10);
				//MessageBox(NULL, strToSend, L"toSend", NULL);
				//MessageBox(NULL, strSent, L"Sent", NULL);
			}
			ret = GetLastError();
			closesocket(client->sock);
			if (ret != 0)
			{
				wchar_t *str = SocketErrorString(ret);
				//MessageBox(NULL, str, L"Err", NULL);
			}
		}
		return ret;
	}
	else
	{
		ULONG ret = ERROR_INVALID_HANDLE;
		char *pCharData = (char *)pData;
	
		*pnBytesSent = send(client->sock, pCharData, nBytesToSend, nFlag);

		if (*pnBytesSent == nBytesToSend)
		{
			ret = ERROR_SUCCESS;
		}
		else
		{
			{	//mid ���Ք�����С��һ�£�ݔ����ֵ
				wchar_t strToSend[25];
				wchar_t strSent[25];
				_itow(nBytesToSend, strToSend, 10);
				_itow(*pnBytesSent, strSent, 10);
				//MessageBox(NULL, strToSend, L"toSend", NULL);
				//MessageBox(NULL, strSent, L"Sent", NULL);
			}
			ret = GetLastError();
			closesocket(client->sock);
			if (ret != 0)
			{
				wchar_t *str = SocketErrorString(ret);
				//MessageBox(NULL, str, L"Err", NULL);
			}
		}
		return ret;
	}
}
ULONG	CSocketWrapperToMt::SocketRecv(PSOCKET_MT client, void * pData, int nBytesToReceive, int *pnBytesReceived, int nFlag)
{
	ULONG ret = ERROR_INVALID_HANDLE;
	char *pCharData = (char *)pData;

	//*pnBytesReceived = recv((SOCKET)client->sock, pCharData, nBytesToReceive, nFlag);

	if (RecvAll((SOCKET)client->sock, pCharData, nBytesToReceive))
	{
		*pnBytesReceived = nBytesToReceive;
		ret = ERROR_SUCCESS;
	}
	else
	{	
		{	//mid ���Ք�����С��һ�£�ݔ����ֵ
			wchar_t strToReceive[25];
			wchar_t strReceived[25];
			_itow(nBytesToReceive, strToReceive, 10);
			_itow(*pnBytesReceived, strReceived, 10);
			//MessageBox(NULL, strToReceive, L"toReceive", NULL);
			//MessageBox(NULL, strReceived, L"Received", NULL);
		}
		ret = GetLastError();
		if (ret != 0)
		{
			wchar_t *str = SocketErrorString(ret);
			MessageBox(NULL, str, L"Err", NULL);
		}
	}
	return ret;
}
