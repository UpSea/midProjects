#pragma once
#pragma pack(1)
//mid 以下新添加，只用於此dll和mt之間交流

#define	SOCKET_STATUS_CLIENT_CONNECTED			1
#define	SOCKET_STATUS_CLIENT_DISCONNECTED		2

#define	SOCKET_STATUS_SERVER_LISTENING			3
#define	SOCKET_STATUS_SERVER_NOTLISTENING		4
typedef struct _SOCKET_CLIENT
{
	BYTE status;
	USHORT sequence;
	ULONG sock;
} SOCKET_MT, *PSOCKET_MT;

#pragma pack()

