def addValuesFromCSV():
    """
    mid 获得数据并便利检索数据
    """
    from pyalgotrade.feed import csvfeed
    feed = csvfeed.Feed("Date", "%Y-%m-%d")
    feed.addValuesFromCSV("quandl_gold_2.csv")
    for dateTime, value in feed:
        print dateTime, value
def addYahooCSV():
    """
    mid 获得数据并遍历检索数据
    """
    from pyalgotrade.barfeed import yahoofeed
    # Load the yahoo feed from the CSV file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("orcl", "orcl-2000.csv")    
    feedDataSeries = feed.getDataSeries()
    feedDataSerie = feedDataSeries.getCloseDataSeries()     
    for time,bars in feed:
        bar = bars["orcl"]
        print "time:%s,open:%s,close:%s" % (time,bar.getClose(),bar.getClose())

addValuesFromCSV()
addYahooCSV()