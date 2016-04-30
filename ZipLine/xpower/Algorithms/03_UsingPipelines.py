# The pipeline API requires imports.
#from quantopian.pipeline import Pipeline
#from quantopian.algorithm import attach_pipeline, pipeline_output
#from quantopian.pipeline.data.builtin import USEquityPricing
#from quantopian.pipeline.factors import SimpleMovingAverage
from zipline.pipeline import Pipeline
#from zipline.algorithm import attach_pipeline, pipeline_output
from zipline.pipeline.data import USEquityPricing
from numpy import float64
from zipline.pipeline.data import Column
from zipline.pipeline.data import DataSet
from zipline.pipeline.factors import SimpleMovingAverage
import logging
import zipline as zp

log = logging.getLogger("mid'logger")# 创建一个logger
log.setLevel(logging.DEBUG)
fh = logging.FileHandler('test.log')# 创建一个handler，用于写入日志文件
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()# 再创建一个handler，用于输出到控制台
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')# 定义handler的输出格式
fh.setFormatter(formatter)
ch.setFormatter(formatter)
log.addHandler(fh)# 给logger添加handler
log.addHandler(ch)
log.info('A new backtest starts')# 记录一条日志

class DualEmaTalib(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        super(DualEmaTalib, self).__init__(*args, **kwargs)    #mid 采用super(child,self).method()格式调用某个类的父类的方法。        
    def initialize(context):
        # Create, register and name a pipeline in initialize.
        pipe = Pipeline()
        context.attach_pipeline(pipe, 'AAPL')
    
        # Construct a simple moving average factor and add it to the pipeline.
        USEquityPricing需要本地自定义
        if True:
            sma_short = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10)
        else:#mid added
            data = Column(float64)
            dataset = DataSet()
            close = data.bind(dataset, 'aapl')
            sma_short = SimpleMovingAverage(inputs=[close], window_length=10)

        
        pipe.add(sma_short, 'sma_short')
    
        # Set a screen on the pipelines to filter out securities.
        #pipe.set_screen(sma_short > 1.0)    
        
    def before_trading_start(context, data):
        # Pipeline_output returns the constructed dataframe.
        output = context.pipeline_output('AAPL')
        print(output)
        # Select and update your universe.
        context.my_universe = output.sort('sma_short', ascending=False).iloc[:200]
        #update_universe(context.my_universe.index) 
        if(len(context.my_universe.index)>0):
            context.trading_client.update_universe(context.my_universe.index)            
    def handle_data(context, data):
        output = context.pipeline_output('AAPL')
        print(output)        
        log.info("\n" + str(context.my_universe.head(5)))
          
if __name__ == '__main__':
    import sys
    sys.path.append('/home/mid/PythonProjects/xpower')      
    
    import zipline.utils.factory as zpf
    from datetime import datetime
    import matplotlib.pyplot as plt
    
    data = zpf.load_from_yahoo(stocks=['AAPL'],
                               indexes={},
                               start=datetime(2015, 1, 1),
                               end=datetime(2016, 3, 5),
                               adjusted=True)
    #get_loader : callable
        #A function that is given an atomic term and returns a PipelineLoader
        #to use to retrieve raw data for that term.
    from zipline.pipeline.loaders.equity_pricing_loader import USEquityPricingLoader
    
    
    
    class raw_price_loader():
        def __init__(self, *args, **kwargs):
            from TradingCalendar import shTradingCalendar
            tradingcalendar = shTradingCalendar     
            self._calendar = tradingcalendar.trading_day.copy()
        
    def adjustments_loader():
        pass
    raw_price_loader=raw_price_loader()
    def get_pipeline_loader(term):
        return USEquityPricingLoader(raw_price_loader, adjustments_loader)
    get_pipeline_loader = get_pipeline_loader
    algo = DualEmaTalib(instant_fill=False,
                          capital_base=50000,
                          env=None,
                          sim_params = None,  # 设置有此参数时，start和end不能再设置，否则，显得多余也会运行assert错误
                          #start = algo['start'],
                          #end = algo['end'],
                          data_frequency = 'daily',
                          get_pipeline_loader = get_pipeline_loader)
    def dumpDict(dictStr):
        """"""
        import json
        jsonDumpsIndentStr = json.dumps(dictStr, indent=4,skipkeys = False,default=str,sort_keys=True)
        print (jsonDumpsIndentStr) 
    def analyze(data,  results):
        fig = plt.figure()
        ax1 = fig.add_subplot(211, ylabel='Price in $')
        data.plot(ax=ax1, color='r', lw=2.)
        '''
        results[['stock_price', 'average_price']].plot(ax=ax1, lw=2.)
        ax1.plot( results.ix[ results.buy].index,  results.average_price[ results.buy],
                 '^', markersize=10, color='m')
        ax1.plot( results.ix[ results.sell].index,  results.average_price[ results.sell],
                 'v', markersize=10, color='k')
        '''
        ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')        
        results.portfolio_value.plot(ax=ax2, lw=2.)
        '''
        ax2.plot( results.ix[ results.buy].index,
                  results.portfolio_value[ results.buy],
                 '^', markersize=10, color='m')
        ax2.plot( results.ix[ results.sell].index,
                  results.portfolio_value[ results.sell],
                 'v', markersize=10, color='k')        
        '''
        plt.legend(loc=0)
        plt.gcf().set_size_inches(14, 10)    
    algo.dumpDict = dumpDict
    algo.data = data
    results = algo.run(data)
    analyze(data,results)
    plt.show()