#include "stdafx.h"
#include "InterfaceToMT.h"
#include "Mt5Client.h"


CMt5Client::CMt5Client()
{
	{	//mid 1)初始化 Socket Dll，由于Local和Remote都有可能用到Tcp调用，所以安排在此
		int		err;
		WORD    wVersionRequested;
		WSADATA wsaData;

		wVersionRequested = MAKEWORD(2, 2);
		err = WSAStartup(wVersionRequested, &wsaData);
		if (err != 0)	//mid ==0表示成功
		{//mid 失败
			//return FALSE;
		}
	}
}

CMt5Client::~CMt5Client()
{
	{	//mid 3）清理Socket
		WSACleanup();
	}
}


CString CMt5Client::RequestKDataThread(LPVOID pParam)
{
	struct aa
	{
		CString port;
		CString ip;
		CString symbol;
		EnumReqHistoryDataType ktype;
	} mtBroker;
	mtBroker.port = CString("5050");
	mtBroker.ip = CString("192.168.0.212");
	mtBroker.symbol = CString("XAUUSD");
	mtBroker.ktype = HistoryPeriodD1;

	//mid 以下为TcpClient变量(本程序客户端，用于连接Mt5TcpServer)
	BOOL	bIsConnected = TRUE;
	BOOL	bReturn = FALSE;
	int		iTimesAlreadyConnected = 0;	//mid 已连接次数
	const	int	iTimesToConnect = 1;	//mid 尝试连接次数，超过次数之后，不在连接，并标注连接失败

	SOCKET			socketRequest;
	sockaddr_in		socketClientAddr;		//mid 远端Mt5TcpServerSocket地址

	//mid 1)设置将要连接的服务器地址
	//mid 獲取Port
	int iPort = _ttol(mtBroker.port);
	//mid 獲取Ip
	char szIp[30];
	memset(szIp, 0, sizeof(szIp));
	wcstombs(szIp, mtBroker.ip, mtBroker.ip.GetLength() * 2);
	//unsigned long lIp = ntohl(inet_addr(szIp));



	socketClientAddr.sin_addr.s_addr = inet_addr(szIp);
	socketClientAddr.sin_family = AF_INET;
	socketClientAddr.sin_port = htons(iPort); //5000;		
	//mid 2)创建socket
	socketRequest = socket(AF_INET, SOCK_STREAM, 0);

	/*mid
	此两方法成对出现，一个使有效，一个使无效
	CreateSocketClient("192.168.1.212", 5000);
	closesocket(m_SocketClient);
	*/
	while (connect(socketRequest, (sockaddr*)&(socketClientAddr), sizeof(socketClientAddr)))
	{//连接到服务器
		DWORD dwErr;
		dwErr = GetLastError();
		if (10056 == dwErr)
		{	//mid 在一个已连接的套接字上面进行连接，说明在Connect()函数中已有connect()成功
			bIsConnected = TRUE;
			break;
		}

		if (iTimesAlreadyConnected>iTimesToConnect)
		{	//mid 尝试连接
			bIsConnected = FALSE;
			AfxMessageBox(TEXT("Connect() Connect Error."));
			break;
		}
		iTimesAlreadyConnected++;
	}
	if (bIsConnected)
	{
		TRACE("\n连接成功\n");
		REQ_HEADER reqHeader;
		reqHeader.ReqType = ReqTypeHistory;
		if (send(socketRequest, (char*)&reqHeader, sizeof(REQ_HEADER), 0) == sizeof(REQ_HEADER))
		{
			TRACE("\n请求类型数据头发送成功\n");
			REQ_HISTORY reqHistory;
			memset(&reqHistory, 0, sizeof(REQ_HISTORY));
			//mid 1）将UNICODE字串转化为utf8
			char * szSymbol = UnicodeToUTF_8First(mtBroker.symbol);
			strncpy(reqHistory.symbol, szSymbol, min(sizeof(reqHistory.symbol) / 2/*mid 只能假設每個字符佔用2個字節，防止溢出*/, mtBroker.symbol.GetLength()));
			//mid 2）释放转换结果
			delete[] szSymbol;
			//strncpy(reqHistory.symbol, "XAUUSD", min(sizeof(reqHistory.symbol) / 2/*mid 只能假設每個字符佔用2個字節，防止溢出*/, mtBroker.symbol.GetLength()));
			reqHistory.type = mtBroker.ktype;
			int iSizeOfReqHistory = sizeof(REQ_HISTORY);
			if (send(socketRequest, (char*)&reqHistory, sizeof(REQ_HISTORY), 0) == sizeof(REQ_HISTORY))
			{
				TRACE("\n历史数据请求发送成功\n");
				RSP_HISTORY_HEADER rspHistoryHeader;
				memset(&rspHistoryHeader, 0, sizeof(RSP_HISTORY_HEADER));
				if (recv(socketRequest, (char*)&rspHistoryHeader, sizeof(RSP_HISTORY_HEADER), 0) == sizeof(RSP_HISTORY_HEADER))
				{
					TRACE("\n历史数据数据头接收成功\n");
					EnumReqHistoryDataType	rspKType = rspHistoryHeader.m_type;
					CString					strRspSymbol = Utf_8ToUnicode(rspHistoryHeader.m_szSymbol);
					int						nRspCount = rspHistoryHeader.m_nCount;
					if (rspKType == mtBroker.ktype && mtBroker.symbol.CompareNoCase(strRspSymbol) == 0)
					{
						RSP_HISTORY *pHistoryArray = new RSP_HISTORY[nRspCount];		//mid 据answer描述的数据大小定义数组大小，需要手动删除掉
						int const nTotalBytesToReceive = nRspCount*sizeof(RSP_HISTORY);		//mid 待接收数据总量，
						memset(pHistoryArray, 0, nTotalBytesToReceive);

						if (RecvAll(socketRequest, pHistoryArray, nTotalBytesToReceive))
						{
							TRACE("\n历史数据接收成功\n");
							CString KData;
							for (int i = 0; i < nRspCount; i++)											//mid 按 [0,9] 共10个数循环	获得MT 发来数据。
							{																							//mid 装载	下标：[1,10]，剩余下标[11],有何深意？？，无用，已去除。
								//mid 1）获得code
								//strncpy(pKData[i].m_szCode, strRspSymbol, min(sizeof(pKData[i].m_szCode), strRspSymbol.GetLength()));
								//mid 2）获得时间
								MqlDateTime MqlTime = pHistoryArray[i].m_time;
								CTime timeReceived(MqlTime.year, MqlTime.mon, MqlTime.day, MqlTime.hour, MqlTime.min, MqlTime.sec);
								CString timeStr = timeReceived.Format("\n%Y年%m月%d日%H时%M分%S秒\n");
								//TRACE(timeStr);
								//pKDATA[i].m_qwTime = ToStockTime(&timeReceived);
								//mid 3）获得数值数据
								int m_dOpen = pHistoryArray[i].m_fOpen;	//mid 开始 OHLCVA数据,原先是要*0.001，是因数据在网上发送时使用整数（*1000），在此还原
								int m_dHigh = pHistoryArray[i].m_fHigh;	//mid MT数据暂时没有如此处理，所以不用转换。
								int m_dLow = pHistoryArray[i].m_fLow;
								int m_dClose = pHistoryArray[i].m_fClose;
								int m_llVolume = pHistoryArray[i].m_fVolume;
								int m_dAmount = pHistoryArray[i].m_fAmount;



								CString str;
								str.Format(CString("%s,%d,%d,%d,%d,%d,%d\r\n"), timeStr, m_dOpen, m_dHigh, m_dLow, m_dClose, m_llVolume, m_dAmount);
								KData = KData + str;


							}
							delete[] pHistoryArray;

							return KData;
							//---02
							//mid 以上数据准备完毕，以下准备发送
							//UINT nMsgType = CStock::dataK;//mid 發送的數據的類型
							//::SendMessage(pMt5->m_hExchangerWnd, pMt5->m_uiNewDataMsg, nMsgType, (LPARAM)(pKData));
						}
						else
						{
							TRACE("\n历史数据接收失败\n");
						}
						//mid 无条件释放数据接收缓存
						delete[] pHistoryArray;
					}
					else
					{
						AfxMessageBox(TEXT("Responded Error History Data KType."));
					}
				}
				else
				{
					DWORD dwErr;
					dwErr = GetLastError();
					TRACE(TEXT("\n历史数据数据头接收失败\n"));
				}
			}
			else
			{
				DWORD dwErr;
				dwErr = GetLastError();
				TRACE(TEXT("\n历史数据请求发送失败\n"));
			}
		}
		else
		{
			DWORD dwErr;
			dwErr = GetLastError();
			TRACE("\n请求类型数据头发送失败\n");
		}
	}
	else
	{
		DWORD dwErr;
		dwErr = GetLastError();
		CString str;
		str.Format(TEXT("\n连接失败,ErrorNo:%d\n"), dwErr);
		TRACE(str);
	}
	closesocket(socketRequest);
	AfxEndThread(0);
	return 0;
}
CString CMt5Client::Utf_8ToUnicode(char* szU8)
{
	//UTF8 to Unicode
	//mt5中字符编码使用utf8，本项目使用的是unicode，所以需要转化方能显示

	//预转换，得到所需空间的大小
	int wcsLen = ::MultiByteToWideChar(CP_UTF8, NULL, szU8, strlen(szU8), NULL, 0);
	//分配空间要给'\0'留个空间，MultiByteToWideChar不会给'\0'空间
	wchar_t* wszString = new wchar_t[wcsLen + 1];
	//转换
	::MultiByteToWideChar(CP_UTF8, NULL, szU8, strlen(szU8), wszString, wcsLen);
	//最后加上'\0'
	wszString[wcsLen] = '\0';

	//mid 自动变量接收结果，清理堆内存
	CString 	str = wszString;
	delete[] wszString;

	return str;
}
char*CMt5Client::UnicodeToUTF_8First(CString str)
{
	//mid 将UNICODE的CString转换为utf8字符串返回，在此处使用的是堆内存分配，所以，接受者在使用完结果后需要手动释放内存，以防溢出
	int u8Len = WideCharToMultiByte(CP_UTF8, NULL, CStringW(str), str.GetLength(), NULL, 0, NULL, NULL);
	char* szU8 = new  char[u8Len + 1];
	WideCharToMultiByte(CP_UTF8, NULL, CStringW(str), str.GetLength(), szU8, u8Len, NULL, NULL);
	szU8[u8Len] = '\0';
	return szU8;
}

BOOL CMt5Client::Logout(void)
{
	struct aa
	{
		CString port;
		CString ip;
		CString symbol;
		CString brokerName;
		CString accountName;
		CString password;
		EnumReqHistoryDataType ktype;
	} mtBroker;
	mtBroker.port = CString("5050");
	mtBroker.ip = CString("192.168.0.212");
	mtBroker.symbol = CString("XAUUSD");
	mtBroker.ktype = HistoryPeriodD1;


	sockaddr_in		socketClientAddr;		//mid 远端Mt5TcpServerSocket地址
	//mid 1)设置将要连接的服务器地址
	//mid 獲取Port
	int iPort = _ttol(mtBroker.port);
	//mid 獲取Ip
	char szIp[30];
	memset(szIp, 0, sizeof(szIp));
	wcstombs(szIp, mtBroker.ip, mtBroker.ip.GetLength() * 2);

	socketClientAddr.sin_addr.s_addr = inet_addr(szIp);
	socketClientAddr.sin_family = AF_INET;
	socketClientAddr.sin_port = htons(iPort); //5000;	


	long	dTimeStart = clock();
	long	dTimeNow = clock();
	long	dTimeLastEnd = clock();
	BOOL	bIsConnected = TRUE;

	SOCKET			socketClientConnection;			//mid 本地客户端，用于和Mt5TcpServerSocket建立连接
	socketClientConnection = socket(AF_INET, SOCK_STREAM, 0);


	int		iTimesAlreadyConnected = 0;	//mid 已连接次数
	const	int	iTimesToConnect = 1;	//mid 尝试连接次数，超过次数之后，不在连接，并标注连接失败
	/*mid
	此两方法成对出现，一个使有效，一个使无效
	CreateSocketClient("192.168.1.212", 5000);
	closesocket(m_SocketClient);
	*/


	while (connect(socketClientConnection, (sockaddr*)&(socketClientAddr), sizeof(socketClientAddr)))
	{//连接到服务器
		//return (m_dTimeNow - m_dTimeStart) / CLOCKS_PER_SEC;	//mid 返回经过的秒数，原先为微秒
		//CString timeStr = timeReceived.Format("%Y年%m月%d日%H时%M分%S秒\r\n");
		if (iTimesAlreadyConnected>iTimesToConnect)
		{	//mid 尝试连接
			bIsConnected = FALSE;

			DWORD dwErr;
			dwErr = GetLastError();

			AfxMessageBox(TEXT("Logout() Connect Error."));
			break;
		}
		dTimeNow = clock();
		//CString strTimeAll;
		//strTimeAll.Format("\n已总共连接时间：%d\n", dTimeNow - dTimeStart);
		//TRACE(strTimeAll);
		CString strTimeThisPeriod;
		strTimeThisPeriod.Format(TEXT("\n本循环连接时间：%d ms\n"), dTimeLastEnd - dTimeNow);

		TRACE(strTimeThisPeriod);
		dTimeLastEnd = clock();
		Sleep(100);
		iTimesAlreadyConnected++;
	}
	if (bIsConnected)
	{
		TRACE("\n连接成功\n");
		REQ_HEADER reqHeader;
		reqHeader.ReqType = ReqTypeLogout;
		if (send(socketClientConnection, (char*)&reqHeader, sizeof(REQ_HEADER), 0) == sizeof(REQ_HEADER))
		{
			TRACE("\n请求类型数据头发送成功\n");
			REQ_LOGOUT reqLogout;
			memset(&reqLogout, 0, sizeof(REQ_LOGOUT));

			CString strBrokerName = mtBroker.brokerName;
			CString strAccount = mtBroker.accountName;
			CString strPassword = mtBroker.password;

			strncpy(reqLogout.broker, "", min(sizeof(reqLogout.broker), strBrokerName.GetLength()));
			strncpy(reqLogout.account, "", min(sizeof(reqLogout.account), strAccount.GetLength()));
			strncpy(reqLogout.password, "", min(sizeof(reqLogout.password), strPassword.GetLength()));

			if (send(socketClientConnection, (char*)&reqLogout, sizeof(REQ_LOGOUT), 0) == sizeof(REQ_LOGOUT))
			{
				TRACE("\n账户密码数据发送成功\n");
				RSP_LOGOUT rspLogout;
				memset(&rspLogout, 0, sizeof(RSP_LOGOUT));
				if (recv(socketClientConnection, (char*)&rspLogout, sizeof(RSP_LOGOUT), 0) == sizeof(RSP_LOGOUT))
				{
					TRACE("\n登录数据数据反馈接收成功\n");
					CString					strRsp = Utf_8ToUnicode(rspLogout.result);
					if (strRsp.CompareNoCase(TEXT("TRUE")) == 0)
					{
						return TRUE;
					}
					else
					{
						return FALSE;
					}
				}
				else
				{
					DWORD dwErr;
					dwErr = GetLastError();
					TRACE("\n登录数据数据反馈接收失败\n");
				}
			}
			else
			{
				DWORD dwErr;
				dwErr = GetLastError();
				TRACE("\n账户密码数据发送失败\n");
			}

		}
		else
		{
			DWORD dwErr;
			dwErr = GetLastError();
			TRACE("\n请求类型数据头发送失败\n");
		}
	}
	else
	{
		DWORD dwErr;
		dwErr = GetLastError();
		CString str;
		str.Format(TEXT("\n连接失败,ErrorNo:%d\n"), dwErr);
		TRACE(str);
	}
	closesocket(socketClientConnection);
	return TRUE;
}

BOOL CMt5Client::RecvAll(SOCKET sock, void *buf, int size)
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

CString CMt5Client::RequestCodeThread(LPVOID pParam)
{
	//CRemoteDataTcpMt5 * pMt5 = (CRemoteDataTcpMt5 *)pParam;
	struct aa{ CString port; CString ip; } mtBroker;
	mtBroker.port = CString("5050");
	mtBroker.ip = CString("192.168.0.212");
	//mid 以下为TcpClient变量(本程序客户端，用于连接Mt5TcpServer)
	BOOL	bIsConnected = TRUE;
	BOOL	bReturn = FALSE;
	int		iTimesAlreadyConnected = 0;	//mid 已连接次数
	const	int	iTimesToConnect = 1;	//mid 尝试连接次数，超过次数之后，不在连接，并标注连接失败

	SOCKET			socketRequest;
	sockaddr_in		socketClientAddr;		//mid 远端Mt5TcpServerSocket地址

	//mid 1)设置将要连接的服务器地址
	//mid 獲取Port
	int iPort = _ttol(mtBroker.port);
	//mid 獲取Ip
	char szIp[30];
	memset(szIp, 0, sizeof(szIp));
	wcstombs(szIp, mtBroker.ip, mtBroker.ip.GetLength() * 2);
	//unsigned long lIp = ntohl(inet_addr(szIp));



	socketClientAddr.sin_addr.s_addr = inet_addr(szIp);
	socketClientAddr.sin_family = AF_INET;
	socketClientAddr.sin_port = htons(iPort); //5000;		
	//mid 2)创建socket
	socketRequest = socket(AF_INET, SOCK_STREAM, 0);

	/*mid
	此两方法成对出现，一个使有效，一个使无效
	CreateSocketClient("192.168.1.212", 5000);
	closesocket(m_SocketClient);
	*/
	while (connect(socketRequest, (sockaddr*)&(socketClientAddr), sizeof(socketClientAddr)))
	{//连接到服务器
		DWORD dwErr;
		dwErr = GetLastError();
		if (10056 == dwErr)
		{	//mid 在一个已连接的套接字上面进行连接，说明在Connect()函数中已有connect()成功
			bIsConnected = TRUE;
			break;
		}

		if (iTimesAlreadyConnected>iTimesToConnect)
		{	//mid 尝试连接
			bIsConnected = FALSE;
			AfxMessageBox(TEXT("Connect() Connect Error."));
			break;
		}
		iTimesAlreadyConnected++;
	}
	if (bIsConnected)
	{
		TRACE("\n连接成功\n");
		REQ_HEADER reqHeader;
		reqHeader.ReqType = ReqTypeCode;
		if (send(socketRequest, (char*)&reqHeader, sizeof(REQ_HEADER), 0) == sizeof(REQ_HEADER))
		{
			TRACE("\n请求类型数据头发送成功\n");
			RSP_CODE_HEADER rspCodeHeader;
			memset(&rspCodeHeader, 0, sizeof(RSP_CODE_HEADER));
			if (recv(socketRequest, (char*)&rspCodeHeader, sizeof(RSP_CODE_HEADER), 0) == sizeof(RSP_CODE_HEADER))
			{
				TRACE("\n历史数据数据头接收成功\n");
				CString 	strRspBroker = Utf_8ToUnicode(rspCodeHeader.m_szBroker);
				CString		strRspAccount = Utf_8ToUnicode(rspCodeHeader.m_szAccount);
				int			nRspCount = rspCodeHeader.m_nCount;
				//if (strRspBroker.CompareNoCase(pMt5->GetBrokerName() ) ==0 && strRspAccount.CompareNoCase(pMt5->GetAccountName()) == 0)
				if (TRUE)
				{
					RSP_CODE *pHistoryArray = new RSP_CODE[nRspCount];		//mid 据answer描述的数据大小定义数组大小，需要手动删除掉
					int const nTotalBytesToReceive = nRspCount*sizeof(RSP_CODE);		//mid 待接收数据总量，
					memset(pHistoryArray, 0, nTotalBytesToReceive);

					if (RecvAll(socketRequest, pHistoryArray, nTotalBytesToReceive))
					{
						TRACE("\nCodes数据接收成功\n");
						CString codes;
						for (int i = 0; i < nRspCount; i++)
						{
							CString str;
							str.Format(CString("%s,%s,%d\r\n"), Utf_8ToUnicode(pHistoryArray[i].m_szCode), Utf_8ToUnicode(pHistoryArray[i].m_szName), pHistoryArray[i].m_iDigits);
							codes = codes + str;
							TRACE(str);
						}
						delete[] pHistoryArray;
						return codes;
					}
					else
					{
						TRACE("\n历史数据接收失败\n");
					}
					//mid 无条件释放数据接收缓存
					delete[] pHistoryArray;
				}
				else
				{
					AfxMessageBox(TEXT("Responded Error History Data KType."));
				}
			}
			else
			{
				DWORD dwErr;
				dwErr = GetLastError();
				TRACE(TEXT("\n历史数据数据头接收失败\n"));
			}
		}
		else
		{
			DWORD dwErr;
			dwErr = GetLastError();
			TRACE("\n请求类型数据头发送失败\n");
		}
	}
	else
	{
		DWORD dwErr;
		dwErr = GetLastError();
		CString str;
		str.Format(TEXT("\n连接失败,ErrorNo:%d\n"), dwErr);
		TRACE(str);
	}
	closesocket(socketRequest);
	AfxEndThread(0);
	return 0;
}
