from pyalgotrade.bitcoincharts import barfeed
from pyalgotrade.tools import resample
from pyalgotrade import bar

import datetime


def main():
    '''
    mid 先要从网站手动下载tick压缩文件
    手动解压后通过此程序转化周期
    '''
    barFeed = barfeed.CSVTradeFeed()
    barFeed.addBarsFromCSV("bitstampUSD.csv", fromDateTime=datetime.datetime(2014, 1, 1),toDateTime=datetime.datetime(2014, 2, 1))
    resample.resample_to_csv(barFeed, bar.Frequency.MINUTE*30, "30min-bitstampUSD.csv")


if __name__ == "__main__":
    main()