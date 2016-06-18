#pragma once
#define	STKLIB_MAX_CODE3		64			// mid added ���ݽϳ���Ʊ����
#define	STKLIB_COMMENT			256
#define	STKLIB_MAX_NAME			16
#define	STKLABEL_LEN			10			// �ɺ����ݳ���,�����г��ɺű������Ǯ��,��TSInterface.h���ж��壬�ڴ���˼򵥰���

#pragma pack(1)

//mid enum section
//mid 01
enum EnumReqType
{
	ReqTypeError = -1,
	ReqTypeReport = 0x00,		//mid ��ѯʵʱ�۸�����
	ReqTypeHistory = 0x01,		//mid ��ѯ��ʷ�۸�����
	ReqTypeTradePosition = 0x02,		//mid ��ѯ��ǰ�˻�ͷ��
	ReqTypeTradeHistory = 0x03,		//mid ��ѯ��ǰ�˻���ʷ���׼�¼
	ReqTypePositionAsy = 0x04,		//mid Ҫ��MTϵͳ��ǰ�˻����ֵ�ͷ��
	ReqTypeOrderAsy = 0x05,		//mid Ҫ��MTϵͳ��ǰ�˻����ֵĹҵ�
	ReqTypeLogin = 0x06,		//mid ��½��Ϣ
	ReqTypeLogout = 0x07,
	ReqTypeConnect = 0x08,
	ReqTypeSubscribe = 0x09,
	ReqTypeUnSubscribe = 0x10,
	ReqTypeCode = 0x11,
	ReqTypeEnd = 0x12,
};
//mid 02
enum EnumReqTradeActionsType
{
	TradeActionDeal = 0x00,    //mid Place a trade order for an immediate execution with the specified parameters (market order)
	TradeActionPending = 0x01,    //mid Place a trade order for the execution under specified conditions (pending order)
	TradeActionSLTP = 0x02,    //mid Modify Stop Loss and Take Profit values of an opened position
	TradeActionModify = 0x03,    //mid Modify the parameters of the order placed previously
	TradeActionRemove = 0x04,    //mid Delete the pending order placed previously
};
//mid 03
enum EnumReqHistoryDataType
{	//mid 20150507192547 �˴�������KData.h��	enum KTypes ������ȫһ��
	//mid �ڴ��ظ����壬��Ϊ����Ϊ�ӿ��ļ�������MT����
	//mid ���ļ���MT��Ҳ�У����Ҷ�����ȫ��ͬ�����벻һ����ͬ�������������������ͬ�����ڴ�Ϊlonglong����MT��Ϊlong��
	HistoryPeriodNone = 0x00,
	HistoryPeriodMin = 0x01,
	HistoryPeriodTick = 0x01,
	HistoryPeriodSec1 = 0x02,
	HistoryPeriodM1 = 0x03,
	HistoryPeriodM5 = 0x04,
	HistoryPeriodM15 = 0x05,
	HistoryPeriodM30 = 0x06,
	HistoryPeriodH1 = 0x07,
	HistoryPeriodH4 = 0x08,
	HistoryPeriodD1 = 0x09,
	HistoryPeriodW1 = 0x10,
	HistoryPeriodMN = 0x11,
	HistoryPeriodMax = 0x11,
};
//mid 04
enum EnumReqOrderType
{
	OrderTypeBuy = 0x00,			//mid Market Buy order
	OrderTypeSell = 0x01,			//mid Market Sell order
	OrderTypeBuyLimit = 0x02,			//mid Buy Limit pending order
	OrderTypeSellLimit = 0x03,			//mid Sell Limit pending order
	OrderTypeBuyStop = 0x04,			//mid Buy Stop pending order
	OrderTypeSellStop = 0x05,			//mid Sell Stop pending order
	OrderTypeBuyStopLimit = 0x06,			//mid Upon reaching the order price, a pending Buy Limit order is places at the StopLimit price
	OrderTypeSellStopLimit = 0x07,			//mid Upon reaching the order price, a pending Sell Limit order is places at the StopLimit price
};
//mid 05
enum EnumReqFillingType
{
	OrderFillingFOK = 0x00,			//mid 
	OrderFillingIOK = 0x01,			//mid 
	OrderFillingReturn = 0x02,			//mid 
};
//mid 06
enum EnumReqOrderTypeTime
{
	OrderTimeGTC = 0x00,			//mid 
	OrderTimeDAY = 0x01,			//mid 
	OrderTimeSpecifiedDay = 0x02,			//mid 
	OrderTimeSpecified = 0x03,			//mid 
};

//mid struct section
//mid 01
struct MqlDateTime
{	//mid ����MTʱ��struct�����Ľṹ�����㽻��ʱ������
	int year;           // Year
	int mon;            // Month
	int day;            // Day
	int hour;           // Hour
	int min;            // Minutes
	int sec;            // Seconds
	int day_of_week;    // Day of week (0-Sunday, 1-Monday, ... ,6-Saturday)
	int day_of_year;    // Day number of the year (January 1st is assigned the number value of zero)
};
//mid 02
struct REQ_HEADER
{//mid ͷ�����ܹ��������еĲ�ѯ���࣬����Ask��Header���������ݵĶ�ȡ��ʽ������ʾ��
	BYTE	ReqType;          //mid ��ѯ���ݵ�����,��ֵΪEnumReqType���ͣ�������C++��Mql5��enum��С�����б𣬲���ֱ��Ƕ�׶���
};
//mid 03
struct REQ_REPORT
{
	char							symbol[STKLIB_MAX_CODE3];
	EnumReqHistoryDataType			type;
};
//mid 04
struct REQ_LOGIN
{
	char							broker[STKLIB_MAX_CODE3];
	char							account[STKLIB_MAX_CODE3];
	char							password[STKLIB_MAX_CODE3];
};
//mid 05
struct REQ_SUBSCRIBE_HEADER
{
	int								counts;
};
//mid 06
struct REQ_UNSUBSCRIBE_HEADER
{
	int								counts;
};
//mid 07
struct REQ_SUBSCRIBE
{
	char							symbol[STKLIB_MAX_CODE3];
};
//mid 08
struct REQ_UNSUBSCRIBE
{
	char							symbol[STKLIB_MAX_CODE3];
};
//mid 09
struct REQ_HISTORY
{
	REQ_LOGIN						reqLogin;
	char							symbol[STKLIB_MAX_CODE3];
	int								m_nCount;
	EnumReqHistoryDataType			type;							//mid KType==Period.
};
//mid 10
struct REQ_TRADE
{
	EnumReqTradeActionsType			action;						// Trade operation type
	long long						magic;						// Expert Advisor ID (magic number)
	long long						order;						// Order ticket
	char							symbol[STKLIB_MAX_CODE3];	// Trade symbol
	double							volume;						// Requested volume for a deal in lots
	double							price;						// Price
	double							stoplimit;					// StopLimit level of the order
	double							sl;							// Stop Loss level of the order
	double							tp;							// Take Profit level of the order
	long long						deviation;					// Maximal possible deviation from the requested price
	EnumReqOrderType				type;						// Order type
	EnumReqFillingType				type_filling;				// Order execution type
	EnumReqOrderTypeTime			type_time;					// Order expiration type
	MqlDateTime						expiration;					// Order expiration time (for the orders of ORDER_TIME_SPECIFIED type)
	char							comment[STKLIB_COMMENT];	// Order comment
};
//mid 11
struct REQ_LOGOUT
{
	char							broker[STKLIB_MAX_CODE3];
	char							account[STKLIB_MAX_CODE3];
	char							password[STKLIB_MAX_CODE3];
};
//mid 12
struct REQ_CONNECT
{
	char							connect[STKLIB_MAX_CODE3];
};
//mid 13
struct RSP_SUBSCRIBE
{
	char							result[STKLIB_MAX_CODE3];
};
//mid 14
struct RSP_UNSUBSCRIBE
{
	char							result[STKLIB_MAX_CODE3];
};
//mid 15
struct RSP_CONNECT
{
	char							connect[STKLIB_MAX_CODE3];
};
//mid 16
struct RSP_LOGIN
{
	char	result[STKLIB_MAX_CODE3];
};
//mid 17
struct RSP_LOGOUT
{
	char	result[STKLIB_MAX_CODE3];
};
//mid 18
struct RSP_CODE_HEADER
{
	char						m_szBroker[STKLIB_MAX_CODE3];
	char						m_szAccount[STKLIB_MAX_CODE3];
	int							m_nCount;
};
//mid 19
struct RSP_HISTORY
{
	MqlDateTime		m_time;							//UCT
	double			m_fOpen;						//����
	double			m_fHigh;						//���
	double			m_fLow;							//���
	double			m_fClose;						//����
	long long		m_fVolume;						//��
	double			m_fAmount;						//��
};
//mid 20
struct RSP_REPORT		//mid ����ṹͬStock.h�ж����REPORT�ǲ�ͬ�ģ��ζ����������MT5����
{
	char				m_szCode[STKLIB_MAX_CODE3];		// ֤ȯ����,��'\0'��β
	char				m_szName[STKLIB_MAX_CODE3];		// ֤ȯ����,��'\0'��β
	char				m_szBrokerName[STKLIB_MAX_CODE3];
	char				m_szAccountName[STKLIB_MAX_CODE3];

	MqlDateTime			m_time;						// ����ʱ��
	DWORD				m_dwFlag;					// ͣ�Ʊ�־

	double				m_fLast;					// ���գ�Ԫ��
	double				m_fOpen;					// �񿪣�Ԫ��
	double				m_fHigh;					// ��ߣ�Ԫ��
	double				m_fLow;						// ��ͣ�Ԫ��
	double				m_fNew;						// ���£�Ԫ��

	unsigned long long	m_fVolume;					// �ɽ������ɣ�
	float				m_fAmount;					// �ɽ��Ԫ��
	double				m_fBuyPrice[5];				// �����1,2,3,4��Ԫ��
	float				m_fBuyVolume[5];			// ������1,2,3,4���ɣ�
	double				m_fSellPrice[5];			// ������1,2,3,4��Ԫ��
	float				m_fSellVolume[5];			// ������1,2,3,4���ɣ�

};
//mid 21
struct RSP_HISTORY_HEADER
{
	char						m_szSymbol[STKLIB_MAX_CODE3];
	int							m_nCount;
	EnumReqHistoryDataType		m_type;
};
//mid 22
struct RSP_CODE
{
	char	m_szCode[STKLIB_MAX_CODE3];
	char	m_szName[STKLIB_MAX_CODE3];
	int		m_iDigits;
};
#pragma pack()

