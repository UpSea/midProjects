#pragma once
#include "CSocketWrapperToMt.h"
#define MT_API __declspec(dllexport)

//#define _DLLAPI extern "C" __declspec(dllexport)
CSocketWrapperToMt g_SocketWrapper;
#ifdef __cplusplus
extern "C"{
#endif
	//mid ����MtTcpClient�{�÷���
	//mid 1)�B��ָ�� ��ַ:�˿� TcpServer
	MT_API  ULONG		WINAPI SocketConnectToServer(PSOCKET_MT client, wchar_t * wc_host, USHORT port);
	//mid 2)�P�]���B����TcpServer��ĳ��Socket

	
	//mid ����MtTcpServer�{�÷���
	//mid 1)������ SocketServer�������� ָ�� ��ַ:�˿�
	MT_API  ULONG		WINAPI SocketListenToClient(PSOCKET_MT server, wchar_t * wc_host, USHORT port);
	//mid 2)�ȴ����Կͻ��˵����ӣ��ڂ� ������pSocketServerListening�ϵȴ��B�ӣ������ѳɹ������B�ӵ�Socket�xֵ�opSocketAccepted
	//mid   ֮�ᣬͨ�^pSocketAccepted�M�Д����հl��
	MT_API  ULONG		WINAPI SocketAcceptClient(PSOCKET_MT pSocketServerListening, PSOCKET_MT pSocketAccepted);


	//mid һ�鹫�÷���
	//mid 1)��ȡ����˵��
	MT_API	wchar_t *	WINAPI SocketErrorString(int error_code);
	//mid 2)�P�]ĳ��Socket
	MT_API	void		WINAPI SocketClose(PSOCKET_MT client);

	//mid 3)ͨ�Ô����հl����	ֻ�����һ����ַ������Ҫ���հl�����Ĵ�С���ɡ���˶��x���ɲ�ͬ�l����݋��dll�����������Y���Զ��x�����·Žomt5
	MT_API	ULONG		WINAPI SocketSend(PSOCKET_MT client, void * pData, int nBytesToWrite, int *pnBytesWriten, int flag);
	MT_API	ULONG		WINAPI SocketRecv(PSOCKET_MT client, void * pData, int nBytesToWrite, int *pnBytesWriten, int flag);
#ifdef __cplusplus
}
#endif
