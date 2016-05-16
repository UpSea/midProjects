


# PyAlgoTrade
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

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import urllib2
import os
import datetime

import pyalgotrade.logger
from pyalgotrade import bar
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.utils import dt


def __adjust_month(month):
    if month > 12 or month < 1:
        raise Exception("Invalid month")
    month -= 1  # Months for yahoo are 0 based
    return month


def download_csv(instrument, begin, end, frequency):
    url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=%s&ignore=.csv" % (instrument, __adjust_month(begin.month), begin.day, begin.year, __adjust_month(end.month), end.day, end.year, frequency)

    f = urllib2.urlopen(url)
    if f.headers['Content-Type'] != 'text/csv':
        raise Exception("Failed to download data: %s" % f.getcode())
    buff = f.read()
    f.close()

    # Remove the BOM
    while not buff[0].isalnum():
        buff = buff[1:]

    return buff
def download_weekly_bars(instrument, fromYear,toYear, csvFile):
    """Download weekly bars from Yahoo! Finance for a given year.

    :param instrument: Instrument identifier.
    :type instrument: string.
    :param year: The year.
    :type year: int.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.
    """

    begin = dt.get_first_monday(year)
    end = dt.get_last_monday(year) + datetime.timedelta(days=6)
    bars = download_csv(instrument, begin, end, "w")
    f = open(csvFile, "w")
    f.write(bars)
    f.close()

def build_feed(instruments, fromYear, toYear, storage, frequency=bar.Frequency.DAY, timezone=None, skipErrors=False):
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
    import tusharefeed  
    import pandas as pd
    #------
    from tushareDataManager import tushareDataCenter
    tsCenter = tushareDataCenter(storage)    
    
    logger = pyalgotrade.logger.getLogger("tusharefinance")
    ret = tusharefeed.Feed()

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
        ret.addBarsFromCSV(tsCenter,instrument)   
        #dat = tsCenter.retriveKDataByCode(instrument,bar.Frequency.DAY)
        #ret.addBarsFromDataFrame(instrument, dat)               
    return ret