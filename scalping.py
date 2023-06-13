import pandas
import datetime
import os
import chart
import indicator
import schedule
from chart import FxOhlc
import time

# コンフィグ
# gdrivepath = '/content/drive/My Drive/stock/' # for google drive
basepath = './'
encode = 'utf-8'
folder = 'ohlc'


ohlc_usdjpy = FxOhlc('USDJPY')
ohlc_eurjpy = FxOhlc('EURJPY')
ohlc_gbpjpy = FxOhlc('GBPJPY')
ohlc_eurusd = FxOhlc('EURUSD')
ohlc_gbpusd = FxOhlc('GBPUSD')


def analyze2(ohlc):
    pass


def analyze():
    # intervals = ['5m', '15m', '1h', '1d', '1wk']
    # periods = ['60d', '60d', '730d', 'max', 'max']
    # currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'NZDJPY', 'CADJPY', 'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'CADUSD']
    # intervals = ['5m']
    # currencies = ['USDJPY']
    
    print(datetime.datetime.now())
    # for ohlc in [ohlc_usdjpy, ohlc_eurjpy, ohlc_gbpjpy, ohlc_eurusd, ohlc_gbpusd]:
    for ohlc in [ohlc_usdjpy, ohlc_eurjpy, ohlc_gbpjpy]:
        # ohlc.append_online_data()
        
        # for ohlc_mx, updated, minute in zip([ohlc.m5, ohlc.m15], [ohlc.m5_updated, ohlc.m15_updated], ['5minutes', '15minutes']):
        #     print (' ', ohlc.ticker, ':', minute, ' - ', updated)
        #     if updated:
        #         ohlc_mx2 = ohlc_mx.copy() 
        #         indicator.add_sigma(ohlc_mx2, [20])
        #         indicator.add_ema(ohlc_mx2, [5, 20, 60])
        #         indicator.add_ema(ohlc_mx2, [4, 12]) # 1分足の中期(20)、長期(60)
        #         indicator.add_ema(ohlc_mx2, [60, 180]) # 15分足の中期(20)、長期(60)
                
        #         latest_mx = ohlc_mx2.iloc[-1]
                
        #         if (latest_mx['Close'] < latest_mx['EMA60']) and (latest_mx['Open'] > latest_mx['EMA60']) and (latest_mx['Close'] < latest_mx['EMA20']) and (latest_mx['Close'] < latest_mx['EMA180']):
        #             print(ohlc.ticker, ':', minute, ': short')
                
        #         if (latest_mx['Close'] > latest_mx['EMA60']) and (latest_mx['Open'] < latest_mx['EMA60']) and (latest_mx['Close'] > latest_mx['EMA20']) and (latest_mx['Close'] > latest_mx['EMA180']):
        #             print(ohlc.ticker, ':', minute, ': long')

        if ohlc.m1_updated:
            print (' ', ohlc.ticker, ':', '1minute', ' - ', ohlc.m1_updated)
            chart = ohlc.m1
            chart = indicator.add_sigma(chart, [20])
            chart = indicator.add_ema(chart, [5, 20, 60])
            chart = indicator.add_ema(chart, [25, 100, 300]) # 5分足の短期、中期、長期
            chart = indicator.add_ema(chart, [75, 300, 900]) # 15分足の短期、中期、長期
            chart = indicator.add_swing_high_low(chart)
            chart = indicator.add_ema_slope(chart, [60])
            
            print(chart.tail(10))
        
        if ohlc.m5_updated:
            print (' ', ohlc.ticker, ':', '5minute', ' - ', ohlc.m5_updated)
            chart = ohlc.m5
            chart = indicator.add_sigma(chart, [20])
            chart = indicator.add_ema(chart, [5, 20, 60])
            chart = indicator.add_ema(chart, [4, 12]) # 1分足の中期、長期
            chart = indicator.add_ema(chart, [15, 60, 180]) # 15分足の短期、中期、長期
            chart = indicator.add_swing_high_low(chart)
        
        if ohlc.m15_updated:
            print (' ', ohlc.ticker, ':', '15minute', ' - ', ohlc.m15_updated)
            chart = ohlc.m15
            chart = indicator.add_ema(chart, [5, 20, 60])
            chart = indicator.add_ema(chart, [20, 80, 240]) # 1時間足の短期、中期、長期
            chart = indicator.add_ema(chart, [80, 320, 1160]) # 4時間足の短期、中期、長期
            
            
            
        # latest_m5 = ohlc_m5.iloc[-1]
        # if (latest_m5['Close'] < latest_m5['EMA20']) and (latest_m5['Open'] > latest_m5['EMA20']):
        #     print(ohlc.ticker, ': short')
        
        # print(ohlc_m5.tail(10))
    
    # ohlc_usdjpy.append_online_data()
    # ohlc_eurjpy.append_online_data()
    # ohlc_gbpjpy.append_online_data()
    # ohlc_eurusd.append_online_data()
    # ohlc_gbpusd.append_online_data()
    
    # chart_m5 = ohlc_usdjpy.m5
    # indicator.add_sigma(chart_m5, [20])
    # indicator.add_ema(chart_m5, [5, 20, 60])
    # indicator.add_ema(chart_m5, [4, 12]) # 1分足の中期(20)、長期(60) 
    # indicator.add_ema(chart_m5, [60, 180]) # 15分足の中期(20)、長期(60)
    # print(chart_m5.tail(10))
    
    
if __name__ == "__main__":
    
    os.system('cls')

    # pandasのprint表示の仕方を設定
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.width', 1000)
        
    while(1):
        analyze()
        time.sleep(30)    

 
 
            
