#define	_CRT_SECURE_NO_DEPRECATE
#include "SocketToMt.h"
#pragma comment(lib, "ws2_32.lib")
#pragma intrinsic(__rdtsc)
/*mid +------------------------------------------------------------------+
	SocketConnectToServer                                      
	������
		1���������������ClientSocket
		2���B��������ָ����ServerSocket Ip:Port
//+------------------------------------------------------------------*/
MT_API  ULONG WINAPI SocketConnectToServer(PSOCKET_MT client, wchar_t * wc_host, USHORT port)
{
	return g_SocketWrapper.SocketConnectToServer(client, wc_host, port);
}
/*mid +------------------------------------------------------------------+
	SocketListenToClient                                      
	������
		1���������������ServerSocket
		2���O ����ָ����ServerSocket IP:Port
//+------------------------------------------------------------------*/

MT_API  ULONG WINAPI SocketListenToClient(PSOCKET_MT server, wchar_t * wc_host, USHORT port)
{
	return g_SocketWrapper.SocketListenToClient(server, wc_host, port);
}

MT_API  ULONG WINAPI SocketAcceptClient(PSOCKET_MT pSocketServerListening,PSOCKET_MT pSocketAccepted)
{
	return g_SocketWrapper.SocketAcceptClient(pSocketServerListening,pSocketAccepted);
}
//+------------------------------------------------------------------+
//|		SocketClose			                                        |
//+------------------------------------------------------------------+
MT_API void WINAPI SocketClose(PSOCKET_MT client)
{
	g_SocketWrapper.SocketClose(client);
}
//+------------------------------------------------------------------+
//|		SocketErrorString                                           |
//+------------------------------------------------------------------+
MT_API wchar_t * WINAPI SocketErrorString(int error_code)
{
	return g_SocketWrapper.SocketErrorString(error_code);
}
//+------------------------------------------------------------------
//|		ͨ�������շ�����
//+------------------------------------------------------------------
MT_API ULONG WINAPI SocketSend(PSOCKET_MT client, void * pData, int nBytesToWrite, int *pnBytesWriten, int nFlag)
{
	return g_SocketWrapper.SocketSend(client, pData, nBytesToWrite, pnBytesWriten, nFlag);
}
MT_API ULONG WINAPI SocketRecv(PSOCKET_MT client, void * pData, int nBytesToWrite, int *pnBytesWriten, int nFlag)
{
	return g_SocketWrapper.SocketRecv(client, pData, nBytesToWrite, pnBytesWriten, nFlag);
}

//+------------------------------------------------------------------+
//|		DllMain				                                        |
//+------------------------------------------------------------------+
BOOL __stdcall DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{	
	WSADATA ws;
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		WSAStartup(0x202, &ws);			
		break;
	case DLL_PROCESS_DETACH:
		WSACleanup();
		break;
	}
	return 1;
}
