#pragma once
#include <windows.h>
#include "InterfaceToMt.h"
class CSocketWrapperToMt
{
public:
	CSocketWrapperToMt();
	virtual ~CSocketWrapperToMt();
private:
	sockaddr_in			m_SocketServAddr;		//mid ���愓����SocketListening��SocketAccepted���õ�IP:PORT��ַ���ƺ�SocketAccepted���Բ��ô�ֵ�����о�
	//SOCKET_MT			m_SocketServMt;
	//SOCKET				m_SocketAccepted;
private:
	ULONG my_rand();
	ULONG Host2Ip(char * host);
	ULONG ConnectToServer(char * host, USHORT port);
	ULONG ListenToClient(char * host, USHORT port);
public:
	ULONG	SocketConnectToServer(PSOCKET_MT client, wchar_t * wc_host, USHORT port);
	ULONG   SocketListenToClient(PSOCKET_MT server, wchar_t * wc_host, USHORT port);
	ULONG   SocketAcceptClient(PSOCKET_MT pSocketServerListening,PSOCKET_MT pSocketAccepted);
	void	SocketClose(PSOCKET_MT client);
	wchar_t * SocketErrorString(int error_code);
	
	ULONG	SocketSend(PSOCKET_MT client, void * pData, int nBytesToSend, int *pnBytesSent, int nFlag);
	ULONG	SocketRecv(PSOCKET_MT client, void * pData, int nBytesToReceive, int *pnBytesReceived, int nFlag);
};
