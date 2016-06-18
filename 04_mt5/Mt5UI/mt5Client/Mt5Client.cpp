#include "stdafx.h"
#include "InterfaceToMT.h"
#include "Mt5Client.h"


CMt5Client::CMt5Client()
{
	{	//mid 1)��ʼ�� Socket Dll������Local��Remote���п����õ�Tcp���ã����԰����ڴ�
		int		err;
		WORD    wVersionRequested;
		WSADATA wsaData;

		wVersionRequested = MAKEWORD(2, 2);
		err = WSAStartup(wVersionRequested, &wsaData);
		if (err != 0)	//mid ==0��ʾ�ɹ�
		{//mid ʧ��
			//return FALSE;
		}
	}
}

CMt5Client::~CMt5Client()
{
	{	//mid 3������Socket
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

	//mid ����ΪTcpClient����(������ͻ��ˣ���������Mt5TcpServer)
	BOOL	bIsConnected = TRUE;
	BOOL	bReturn = FALSE;
	int		iTimesAlreadyConnected = 0;	//mid �����Ӵ���
	const	int	iTimesToConnect = 1;	//mid �������Ӵ�������������֮�󣬲������ӣ�����ע����ʧ��

	SOCKET			socketRequest;
	sockaddr_in		socketClientAddr;		//mid Զ��Mt5TcpServerSocket��ַ

	//mid 1)���ý�Ҫ���ӵķ�������ַ
	//mid �@ȡPort
	int iPort = _ttol(mtBroker.port);
	//mid �@ȡIp
	char szIp[30];
	memset(szIp, 0, sizeof(szIp));
	wcstombs(szIp, mtBroker.ip, mtBroker.ip.GetLength() * 2);
	//unsigned long lIp = ntohl(inet_addr(szIp));



	socketClientAddr.sin_addr.s_addr = inet_addr(szIp);
	socketClientAddr.sin_family = AF_INET;
	socketClientAddr.sin_port = htons(iPort); //5000;		
	//mid 2)����socket
	socketRequest = socket(AF_INET, SOCK_STREAM, 0);

	/*mid
	���������ɶԳ��֣�һ��ʹ��Ч��һ��ʹ��Ч
	CreateSocketClient("192.168.1.212", 5000);
	closesocket(m_SocketClient);
	*/
	while (connect(socketRequest, (sockaddr*)&(socketClientAddr), sizeof(socketClientAddr)))
	{//���ӵ�������
		DWORD dwErr;
		dwErr = GetLastError();
		if (10056 == dwErr)
		{	//mid ��һ�������ӵ��׽�������������ӣ�˵����Connect()����������connect()�ɹ�
			bIsConnected = TRUE;
			break;
		}

		if (iTimesAlreadyConnected>iTimesToConnect)
		{	//mid ��������
			bIsConnected = FALSE;
			AfxMessageBox(TEXT("Connect() Connect Error."));
			break;
		}
		iTimesAlreadyConnected++;
	}
	if (bIsConnected)
	{
		TRACE("\n���ӳɹ�\n");
		REQ_HEADER reqHeader;
		reqHeader.ReqType = ReqTypeHistory;
		if (send(socketRequest, (char*)&reqHeader, sizeof(REQ_HEADER), 0) == sizeof(REQ_HEADER))
		{
			TRACE("\n������������ͷ���ͳɹ�\n");
			REQ_HISTORY reqHistory;
			memset(&reqHistory, 0, sizeof(REQ_HISTORY));
			//mid 1����UNICODE�ִ�ת��Ϊutf8
			char * szSymbol = UnicodeToUTF_8First(mtBroker.symbol);
			strncpy(reqHistory.symbol, szSymbol, min(sizeof(reqHistory.symbol) / 2/*mid ֻ�ܼ��Oÿ���ַ�����2���ֹ�����ֹ���*/, mtBroker.symbol.GetLength()));
			//mid 2���ͷ�ת�����
			delete[] szSymbol;
			//strncpy(reqHistory.symbol, "XAUUSD", min(sizeof(reqHistory.symbol) / 2/*mid ֻ�ܼ��Oÿ���ַ�����2���ֹ�����ֹ���*/, mtBroker.symbol.GetLength()));
			reqHistory.type = mtBroker.ktype;
			int iSizeOfReqHistory = sizeof(REQ_HISTORY);
			if (send(socketRequest, (char*)&reqHistory, sizeof(REQ_HISTORY), 0) == sizeof(REQ_HISTORY))
			{
				TRACE("\n��ʷ���������ͳɹ�\n");
				RSP_HISTORY_HEADER rspHistoryHeader;
				memset(&rspHistoryHeader, 0, sizeof(RSP_HISTORY_HEADER));
				if (recv(socketRequest, (char*)&rspHistoryHeader, sizeof(RSP_HISTORY_HEADER), 0) == sizeof(RSP_HISTORY_HEADER))
				{
					TRACE("\n��ʷ��������ͷ���ճɹ�\n");
					EnumReqHistoryDataType	rspKType = rspHistoryHeader.m_type;
					CString					strRspSymbol = Utf_8ToUnicode(rspHistoryHeader.m_szSymbol);
					int						nRspCount = rspHistoryHeader.m_nCount;
					if (rspKType == mtBroker.ktype && mtBroker.symbol.CompareNoCase(strRspSymbol) == 0)
					{
						RSP_HISTORY *pHistoryArray = new RSP_HISTORY[nRspCount];		//mid ��answer���������ݴ�С���������С����Ҫ�ֶ�ɾ����
						int const nTotalBytesToReceive = nRspCount*sizeof(RSP_HISTORY);		//mid ����������������
						memset(pHistoryArray, 0, nTotalBytesToReceive);

						if (RecvAll(socketRequest, pHistoryArray, nTotalBytesToReceive))
						{
							TRACE("\n��ʷ���ݽ��ճɹ�\n");
							CString KData;
							for (int i = 0; i < nRspCount; i++)											//mid �� [0,9] ��10����ѭ��	���MT �������ݡ�
							{																							//mid װ��	�±꣺[1,10]��ʣ���±�[11],�к����⣿�������ã���ȥ����
								//mid 1�����code
								//strncpy(pKData[i].m_szCode, strRspSymbol, min(sizeof(pKData[i].m_szCode), strRspSymbol.GetLength()));
								//mid 2�����ʱ��
								MqlDateTime MqlTime = pHistoryArray[i].m_time;
								CTime timeReceived(MqlTime.year, MqlTime.mon, MqlTime.day, MqlTime.hour, MqlTime.min, MqlTime.sec);
								CString timeStr = timeReceived.Format("\n%Y��%m��%d��%Hʱ%M��%S��\n");
								//TRACE(timeStr);
								//pKDATA[i].m_qwTime = ToStockTime(&timeReceived);
								//mid 3�������ֵ����
								int m_dOpen = pHistoryArray[i].m_fOpen;	//mid ��ʼ OHLCVA����,ԭ����Ҫ*0.001���������������Ϸ���ʱʹ��������*1000�����ڴ˻�ԭ
								int m_dHigh = pHistoryArray[i].m_fHigh;	//mid MT������ʱû����˴������Բ���ת����
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
							//mid ��������׼����ϣ�����׼������
							//UINT nMsgType = CStock::dataK;//mid �l�͵Ĕ��������
							//::SendMessage(pMt5->m_hExchangerWnd, pMt5->m_uiNewDataMsg, nMsgType, (LPARAM)(pKData));
						}
						else
						{
							TRACE("\n��ʷ���ݽ���ʧ��\n");
						}
						//mid �������ͷ����ݽ��ջ���
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
					TRACE(TEXT("\n��ʷ��������ͷ����ʧ��\n"));
				}
			}
			else
			{
				DWORD dwErr;
				dwErr = GetLastError();
				TRACE(TEXT("\n��ʷ����������ʧ��\n"));
			}
		}
		else
		{
			DWORD dwErr;
			dwErr = GetLastError();
			TRACE("\n������������ͷ����ʧ��\n");
		}
	}
	else
	{
		DWORD dwErr;
		dwErr = GetLastError();
		CString str;
		str.Format(TEXT("\n����ʧ��,ErrorNo:%d\n"), dwErr);
		TRACE(str);
	}
	closesocket(socketRequest);
	AfxEndThread(0);
	return 0;
}
CString CMt5Client::Utf_8ToUnicode(char* szU8)
{
	//UTF8 to Unicode
	//mt5���ַ�����ʹ��utf8������Ŀʹ�õ���unicode��������Ҫת��������ʾ

	//Ԥת�����õ�����ռ�Ĵ�С
	int wcsLen = ::MultiByteToWideChar(CP_UTF8, NULL, szU8, strlen(szU8), NULL, 0);
	//����ռ�Ҫ��'\0'�����ռ䣬MultiByteToWideChar�����'\0'�ռ�
	wchar_t* wszString = new wchar_t[wcsLen + 1];
	//ת��
	::MultiByteToWideChar(CP_UTF8, NULL, szU8, strlen(szU8), wszString, wcsLen);
	//������'\0'
	wszString[wcsLen] = '\0';

	//mid �Զ��������ս����������ڴ�
	CString 	str = wszString;
	delete[] wszString;

	return str;
}
char*CMt5Client::UnicodeToUTF_8First(CString str)
{
	//mid ��UNICODE��CStringת��Ϊutf8�ַ������أ��ڴ˴�ʹ�õ��Ƕ��ڴ���䣬���ԣ���������ʹ����������Ҫ�ֶ��ͷ��ڴ棬�Է����
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


	sockaddr_in		socketClientAddr;		//mid Զ��Mt5TcpServerSocket��ַ
	//mid 1)���ý�Ҫ���ӵķ�������ַ
	//mid �@ȡPort
	int iPort = _ttol(mtBroker.port);
	//mid �@ȡIp
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

	SOCKET			socketClientConnection;			//mid ���ؿͻ��ˣ����ں�Mt5TcpServerSocket��������
	socketClientConnection = socket(AF_INET, SOCK_STREAM, 0);


	int		iTimesAlreadyConnected = 0;	//mid �����Ӵ���
	const	int	iTimesToConnect = 1;	//mid �������Ӵ�������������֮�󣬲������ӣ�����ע����ʧ��
	/*mid
	���������ɶԳ��֣�һ��ʹ��Ч��һ��ʹ��Ч
	CreateSocketClient("192.168.1.212", 5000);
	closesocket(m_SocketClient);
	*/


	while (connect(socketClientConnection, (sockaddr*)&(socketClientAddr), sizeof(socketClientAddr)))
	{//���ӵ�������
		//return (m_dTimeNow - m_dTimeStart) / CLOCKS_PER_SEC;	//mid ���ؾ�����������ԭ��Ϊ΢��
		//CString timeStr = timeReceived.Format("%Y��%m��%d��%Hʱ%M��%S��\r\n");
		if (iTimesAlreadyConnected>iTimesToConnect)
		{	//mid ��������
			bIsConnected = FALSE;

			DWORD dwErr;
			dwErr = GetLastError();

			AfxMessageBox(TEXT("Logout() Connect Error."));
			break;
		}
		dTimeNow = clock();
		//CString strTimeAll;
		//strTimeAll.Format("\n���ܹ�����ʱ�䣺%d\n", dTimeNow - dTimeStart);
		//TRACE(strTimeAll);
		CString strTimeThisPeriod;
		strTimeThisPeriod.Format(TEXT("\n��ѭ������ʱ�䣺%d ms\n"), dTimeLastEnd - dTimeNow);

		TRACE(strTimeThisPeriod);
		dTimeLastEnd = clock();
		Sleep(100);
		iTimesAlreadyConnected++;
	}
	if (bIsConnected)
	{
		TRACE("\n���ӳɹ�\n");
		REQ_HEADER reqHeader;
		reqHeader.ReqType = ReqTypeLogout;
		if (send(socketClientConnection, (char*)&reqHeader, sizeof(REQ_HEADER), 0) == sizeof(REQ_HEADER))
		{
			TRACE("\n������������ͷ���ͳɹ�\n");
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
				TRACE("\n�˻��������ݷ��ͳɹ�\n");
				RSP_LOGOUT rspLogout;
				memset(&rspLogout, 0, sizeof(RSP_LOGOUT));
				if (recv(socketClientConnection, (char*)&rspLogout, sizeof(RSP_LOGOUT), 0) == sizeof(RSP_LOGOUT))
				{
					TRACE("\n��¼�������ݷ������ճɹ�\n");
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
					TRACE("\n��¼�������ݷ�������ʧ��\n");
				}
			}
			else
			{
				DWORD dwErr;
				dwErr = GetLastError();
				TRACE("\n�˻��������ݷ���ʧ��\n");
			}

		}
		else
		{
			DWORD dwErr;
			dwErr = GetLastError();
			TRACE("\n������������ͷ����ʧ��\n");
		}
	}
	else
	{
		DWORD dwErr;
		dwErr = GetLastError();
		CString str;
		str.Format(TEXT("\n����ʧ��,ErrorNo:%d\n"), dwErr);
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
	//mid ����ΪTcpClient����(������ͻ��ˣ���������Mt5TcpServer)
	BOOL	bIsConnected = TRUE;
	BOOL	bReturn = FALSE;
	int		iTimesAlreadyConnected = 0;	//mid �����Ӵ���
	const	int	iTimesToConnect = 1;	//mid �������Ӵ�������������֮�󣬲������ӣ�����ע����ʧ��

	SOCKET			socketRequest;
	sockaddr_in		socketClientAddr;		//mid Զ��Mt5TcpServerSocket��ַ

	//mid 1)���ý�Ҫ���ӵķ�������ַ
	//mid �@ȡPort
	int iPort = _ttol(mtBroker.port);
	//mid �@ȡIp
	char szIp[30];
	memset(szIp, 0, sizeof(szIp));
	wcstombs(szIp, mtBroker.ip, mtBroker.ip.GetLength() * 2);
	//unsigned long lIp = ntohl(inet_addr(szIp));



	socketClientAddr.sin_addr.s_addr = inet_addr(szIp);
	socketClientAddr.sin_family = AF_INET;
	socketClientAddr.sin_port = htons(iPort); //5000;		
	//mid 2)����socket
	socketRequest = socket(AF_INET, SOCK_STREAM, 0);

	/*mid
	���������ɶԳ��֣�һ��ʹ��Ч��һ��ʹ��Ч
	CreateSocketClient("192.168.1.212", 5000);
	closesocket(m_SocketClient);
	*/
	while (connect(socketRequest, (sockaddr*)&(socketClientAddr), sizeof(socketClientAddr)))
	{//���ӵ�������
		DWORD dwErr;
		dwErr = GetLastError();
		if (10056 == dwErr)
		{	//mid ��һ�������ӵ��׽�������������ӣ�˵����Connect()����������connect()�ɹ�
			bIsConnected = TRUE;
			break;
		}

		if (iTimesAlreadyConnected>iTimesToConnect)
		{	//mid ��������
			bIsConnected = FALSE;
			AfxMessageBox(TEXT("Connect() Connect Error."));
			break;
		}
		iTimesAlreadyConnected++;
	}
	if (bIsConnected)
	{
		TRACE("\n���ӳɹ�\n");
		REQ_HEADER reqHeader;
		reqHeader.ReqType = ReqTypeCode;
		if (send(socketRequest, (char*)&reqHeader, sizeof(REQ_HEADER), 0) == sizeof(REQ_HEADER))
		{
			TRACE("\n������������ͷ���ͳɹ�\n");
			RSP_CODE_HEADER rspCodeHeader;
			memset(&rspCodeHeader, 0, sizeof(RSP_CODE_HEADER));
			if (recv(socketRequest, (char*)&rspCodeHeader, sizeof(RSP_CODE_HEADER), 0) == sizeof(RSP_CODE_HEADER))
			{
				TRACE("\n��ʷ��������ͷ���ճɹ�\n");
				CString 	strRspBroker = Utf_8ToUnicode(rspCodeHeader.m_szBroker);
				CString		strRspAccount = Utf_8ToUnicode(rspCodeHeader.m_szAccount);
				int			nRspCount = rspCodeHeader.m_nCount;
				//if (strRspBroker.CompareNoCase(pMt5->GetBrokerName() ) ==0 && strRspAccount.CompareNoCase(pMt5->GetAccountName()) == 0)
				if (TRUE)
				{
					RSP_CODE *pHistoryArray = new RSP_CODE[nRspCount];		//mid ��answer���������ݴ�С���������С����Ҫ�ֶ�ɾ����
					int const nTotalBytesToReceive = nRspCount*sizeof(RSP_CODE);		//mid ����������������
					memset(pHistoryArray, 0, nTotalBytesToReceive);

					if (RecvAll(socketRequest, pHistoryArray, nTotalBytesToReceive))
					{
						TRACE("\nCodes���ݽ��ճɹ�\n");
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
						TRACE("\n��ʷ���ݽ���ʧ��\n");
					}
					//mid �������ͷ����ݽ��ջ���
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
				TRACE(TEXT("\n��ʷ��������ͷ����ʧ��\n"));
			}
		}
		else
		{
			DWORD dwErr;
			dwErr = GetLastError();
			TRACE("\n������������ͷ����ʧ��\n");
		}
	}
	else
	{
		DWORD dwErr;
		dwErr = GetLastError();
		CString str;
		str.Format(TEXT("\n����ʧ��,ErrorNo:%d\n"), dwErr);
		TRACE(str);
	}
	closesocket(socketRequest);
	AfxEndThread(0);
	return 0;
}
