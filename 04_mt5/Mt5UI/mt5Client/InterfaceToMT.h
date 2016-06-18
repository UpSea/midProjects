#pragma once
#define	STKLIB_MAX_CODE3		64			// mid added 兼容较长股票代码
#define	STKLIB_COMMENT			256
#define	STKLIB_MAX_NAME			16
#define	STKLABEL_LEN			10			// 股号数据长度,国内市场股号编码兼容钱龙,在TSInterface.h中有定义，在此如此简单包含

#pragma pack(1)

//mid enum section
//mid 01
enum EnumReqType
{
	ReqTypeError = -1,
	ReqTypeReport = 0x00,		//mid 查询实时价格数据
	ReqTypeHistory = 0x01,		//mid 查询历史价格数据
	ReqTypeTradePosition = 0x02,		//mid 查询当前账户头寸
	ReqTypeTradeHistory = 0x03,		//mid 查询当前账户历史交易记录
	ReqTypePositionAsy = 0x04,		//mid 要求MT系统当前账户保持的头寸
	ReqTypeOrderAsy = 0x05,		//mid 要求MT系统当前账户保持的挂单
	ReqTypeLogin = 0x06,		//mid 登陆信息
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
{	//mid 20150507192547 此处定义与KData.h中	enum KTypes 定义完全一致
	//mid 在此重复定义，是为了作为接口文件方便与MT交流
	//mid 此文件在MT中也有，而且定义完全相同（代码不一定相同，但是数据意义必须相同，如在此为longlong，在MT中为long）
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
{	//mid 参照MT时间struct创建的结构，方便交流时间数据
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
{//mid 头必须能够描述所有的查询种类，并对Ask中Header后续的数据的读取方式做出提示。
	BYTE	ReqType;          //mid 查询数据的种类,其值为EnumReqType类型，但由于C++和Mql5对enum大小定义有别，不能直接嵌套定义
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
	double			m_fOpen;						//开盘
	double			m_fHigh;						//最高
	double			m_fLow;							//最低
	double			m_fClose;						//收盘
	long long		m_fVolume;						//量
	double			m_fAmount;						//额
};
//mid 20
struct RSP_REPORT		//mid 这个结构同Stock.h中定义的REPORT是不同的，次定义仅用来与MT5交流
{
	char				m_szCode[STKLIB_MAX_CODE3];		// 证券代码,以'\0'结尾
	char				m_szName[STKLIB_MAX_CODE3];		// 证券名称,以'\0'结尾
	char				m_szBrokerName[STKLIB_MAX_CODE3];
	char				m_szAccountName[STKLIB_MAX_CODE3];

	MqlDateTime			m_time;						// 交易时间
	DWORD				m_dwFlag;					// 停牌标志

	double				m_fLast;					// 昨收（元）
	double				m_fOpen;					// 今开（元）
	double				m_fHigh;					// 最高（元）
	double				m_fLow;						// 最低（元）
	double				m_fNew;						// 最新（元）

	unsigned long long	m_fVolume;					// 成交量（股）
	float				m_fAmount;					// 成交额（元）
	double				m_fBuyPrice[5];				// 申买价1,2,3,4（元）
	float				m_fBuyVolume[5];			// 申买量1,2,3,4（股）
	double				m_fSellPrice[5];			// 申卖价1,2,3,4（元）
	float				m_fSellVolume[5];			// 申卖量1,2,3,4（股）

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

