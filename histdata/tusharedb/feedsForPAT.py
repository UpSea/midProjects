# -*- coding: utf-8 -*-
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""mid
从csv数据获取PAT feeds。
u用以转换dataFrame到feed，相当于以pandas dataframe 为桥，不再以csv为桥。下一步增加方法直接从数据库中读
"""
from pyalgotrade import bar
from pyalgotrade import dataseries
from pyalgotrade.barfeed import membf
from pyalgotrade.barfeed import common
from pyalgotrade.barfeed.csvfeed import RowParser
from pyalgotrade.utils import dt

import os
import datetime


######################################################################
## Yahoo Finance CSV parser
# Each bar must be on its own line and fields must be separated by comma (,).
#
# Bars Format:
# Date,Open,High,Low,Close,Volume,Adj Close
#
# The csv Date column must have the following format: YYYY-MM-DD
class dataFrameBarFeed(membf.BarFeed):
    """Base class for CSV file based :class:`pyalgotrade.barfeed.BarFeed`.

    .. note::
        This is a base class and should not be used directly.
    """

    def __init__(self, frequency, maxLen=dataseries.DEFAULT_MAX_LEN):
        membf.BarFeed.__init__(self, frequency, maxLen)
        self.__barFilter = None
        self.__dailyTime = datetime.time(0, 0, 0)

    def getDailyBarTime(self):
        return self.__dailyTime

    def setDailyBarTime(self, time):
        self.__dailyTime = time

    def getBarFilter(self):
        return self.__barFilter

    def setBarFilter(self, barFilter):
        self.__barFilter = barFilter
    #使用apply+handler最提高效率，但是层层调用显得麻烦
    def addBarsFromDataFrame(self, instrument,rowParser,df):
        # Load the csv file
        loadedBars = []
        for row in df.iterrows():
            bar_ = rowParser.parseBar(row)
            if bar_ is not None and (self.__barFilter is None or self.__barFilter.includeBar(bar_)):
                loadedBars.append(bar_)
        self.addBarsFromSequence(instrument, loadedBars)
        



class RowParser(RowParser):
    def __init__(self, dailyBarTime, frequency, timezone=None, sanitize=False):
        self.__dailyBarTime = dailyBarTime
        self.__frequency = frequency
        self.__timezone = timezone
        self.__sanitize = sanitize
    def parse_date(self,date):
        # Sample: 2005-12-30
        # This custom parsing works faster than:
        # datetime.datetime.strptime(date, "%Y-%m-%d")
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        ret = datetime.datetime(year, month, day)
        return ret
    def __parseDate(self, dateString):
        ret = self.parse_date(dateString)
        # Time on Yahoo! Finance CSV files is empty. If told to set one, do it.
        if self.__dailyBarTime is not None:
            ret = datetime.datetime.combine(ret, self.__dailyBarTime)
        # Localize the datetime if a timezone was given.
        if self.__timezone:
            ret = dt.localize(ret, self.__timezone)
        return ret

    def getFieldNames(self):
        # It is expected for the first row to have the field names.
        return None

    def getDelimiter(self):
        return ","
    
    #对dataFrame的每行进行操作
    def handler(x):
        pass
    #row的结构 row[0]为时间，string类型。row[1]为Series类型:'open'\high\close\low\volume\amoun或price——change等，前面6项和tushare 对应  
    def parseBar(self, row):
        dateTime = self.__parseDate(row[0]) #date
        close = float(row[1]['close'])
        open_ = float(row[1]['open'])
        high = float(row[1]['high'])
        low = float(row[1]['low'])
        volume = float(row[1]['volume'])
        adjClose = None
        
        if self.__sanitize:
            open_, high, low, close = common.sanitize_ohlc(open_, high, low, close)

        return bar.BasicBar(dateTime, open_, high, low, close, volume, adjClose, self.__frequency)


class Feed(dataFrameBarFeed):
    """A :class:`pyalgotrade.barfeed.csvfeed.BarFeed` that loads bars from CSV files downloaded from Yahoo! Finance.

    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** or **pyalgotrade.bar.Frequency.WEEK**
        are supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
    :type timezone: A pytz timezone.
    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the opposite end.
    :type maxLen: int.

    .. note::
        Yahoo! Finance csv files lack timezone information.
        When working with multiple instruments:

            * If all the instruments loaded are in the same timezone, then the timezone parameter may not be specified.
            * If any of the instruments loaded are in different timezones, then the timezone parameter must be set.
    """

    def __init__(self, frequency=bar.Frequency.DAY, timezone=None, maxLen=dataseries.DEFAULT_MAX_LEN):
        if isinstance(timezone, int):
            raise Exception("timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.")

        if frequency not in [bar.Frequency.DAY, bar.Frequency.WEEK]:
            raise Exception("Invalid frequency.")

        dataFrameBarFeed.__init__(self, frequency, maxLen)
        self.__timezone = timezone
        self.__sanitizeBars = False

    def sanitizeBars(self, sanitize):
        self.__sanitizeBars = sanitize

    def barsHaveAdjClose(self):
        return True

    def addBarsFromDataFrame(self, instrument,dataFrame,timezone=None):
        """Loads bars for a given instrument from a CSV formatted file.
        The instrument gets registered in the bar feed.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param path: The path to the CSV file.
        :type path: string.
        :param timezone: The timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
        :type timezone: A pytz timezone.
        """

        if isinstance(timezone, int):
            raise Exception("timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.")

        if timezone is None:
            timezone = self.__timezone

        rowParser = RowParser(self.getDailyBarTime(), self.getFrequency(), timezone, self.__sanitizeBars)
        dataFrameBarFeed.addBarsFromDataFrame(self, instrument,rowParser,dataFrame)
    def addBarsFromCSV(self,tsCenter,instrument):
        from tushareDataManager import tushareDataCenter
        dat = tsCenter.retriveHistData(storageType = 'csv',symbol = instrument)
        self.addBarsFromDataFrame(instrument, dat)
        
    def build_feed(self,instruments, fromYear, toYear, storage, frequency='D', timezone=None, skipErrors=False):
        """Build and load a :class:`pyalgotrade.barfeed.yahoofeed.Feed` using CSV files downloaded from Yahoo! Finance.
        CSV files are downloaded if they haven't been downloaded before.
    
        :param instruments: Instrument identifiers.
        :type instruments: list.
        :param fromYear: The first year.
        :type fromYear: int.
        :param toYear: The last year.
        :type toYear: int.
        :param storage: The path were the files will be loaded from, or downloaded to.
        :type storage: string.
        :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** or **pyalgotrade.bar.Frequency.WEEK**
            are supported.
        :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
        :type timezone: A pytz timezone.
        :param skipErrors: True to keep on loading/downloading files in case of errors.
        :type skipErrors: boolean.
        :rtype: :class:`pyalgotrade.barfeed.yahoofeed.Feed`.
        """
        import pandas as pd
        import pyalgotrade.logger
        
        #------
        from tushareDataManager import tushareDataCenter
        tsCenter = tushareDataCenter(storage)    
        
        logger = pyalgotrade.logger.getLogger("tusharefinance")
    
        if not os.path.exists(storage):
            logger.info("Creating %s directory" % (storage))
            os.mkdir(storage)
    
        for instrument in instruments:
                    
            if(not tsCenter.exists(instrument,frequency)):
                logger.info("Downloading %s from %d to %d" % (instrument, fromYear,toYear))
                try:
                    if frequency == bar.Frequency.DAY:
                        if tsCenter.downloadAndStoreKDataByCode(instrument,fromYear,toYear):
                            logger.info("Downloading successed.")
                        else:
                            logger.info("Downloading failed.")
                    elif frequency == bar.Frequency.WEEK:
                        if(tsCenter.downloadAndStoreKDataByCode(instrument,fromYear,toYear)):
                            logger.info("Downloading successed.")
                        else:
                            logger.info("Downloading failed.")
                    else:
                        raise Exception("Invalid frequency")
                except Exception, e:
                    if skipErrors:
                        logger.error(str(e))
                        continue
                    else:
                        raise e
            else:
                logger.info("\n%s already existed." % (instrument))
            self.addBarsFromCSV(tsCenter,instrument)   
            #dat = tsCenter.retriveKDataByCode(instrument,bar.Frequency.DAY)
            #ret.addBarsFromDataFrame(instrument, dat)               
        return self    