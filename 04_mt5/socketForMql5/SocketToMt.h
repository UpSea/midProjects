#pragma once
#include "CSocketWrapperToMt.h"
#define MT_API __declspec(dllexport)

//#define _DLLAPI extern "C" __declspec(dllexport)
CSocketWrapperToMt g_SocketWrapper;
#ifdef __cplusplus
extern "C"{
#endif
	//mid 以下為MtTcpClient調用方法
	//mid 1)連接指定 地址:端口 TcpServer
	MT_API  ULONG		WINAPI SocketConnectToServer(PSOCKET_MT client, wchar_t * wc_host, USHORT port);
	//mid 2)關閉已連接至TcpServer的某個Socket

	
	//mid 以下為MtTcpServer調用方法
	//mid 1)创建偵聽SocketServer，并侦听 指定 地址:端口
	MT_API  ULONG		WINAPI SocketListenToClient(PSOCKET_MT server, wchar_t * wc_host, USHORT port);
	//mid 2)等待来自客户端的连接，在偵聽服務器pSocketServerListening上等待連接，并將已成功接收連接的Socket賦值給pSocketAccepted
	//mid   之後，通過pSocketAccepted進行數據收發。
	MT_API  ULONG		WINAPI SocketAcceptClient(PSOCKET_MT pSocketServerListening, PSOCKET_MT pSocketAccepted);


	//mid 一下為公用方法
	//mid 1)获取错误说明
	MT_API	wchar_t *	WINAPI SocketErrorString(int error_code);
	//mid 2)關閉某個Socket
	MT_API	void		WINAPI SocketClose(PSOCKET_MT client);

	//mid 3)通用數據收發函數	只需傳入一個地址，和需要被收發數據的大小即可。如此定義，可不同頻繁編輯此dll，而將數據結構自定義權利下放給mt5
	MT_API	ULONG		WINAPI SocketSend(PSOCKET_MT client, void * pData, int nBytesToWrite, int *pnBytesWriten, int flag);
	MT_API	ULONG		WINAPI SocketRecv(PSOCKET_MT client, void * pData, int nBytesToWrite, int *pnBytesWriten, int flag);
#ifdef __cplusplus
}
#endif
