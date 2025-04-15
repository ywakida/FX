""" 売買戦略に対する勝率のシミュレーションを行う
"""
import pandas
import datetime
import os
import chart
import indicator
import schedule
from chart import FxOhlc
import time
import chart_plot

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
    currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'NZDJPY', 'CADJPY', 'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'CADUSD']
    # intervals = ['5m']
    # currencies = ['USDJPY']
    
    print(datetime.datetime.now())
    # for ohlc in [ohlc_usdjpy, ohlc_eurjpy, ohlc_gbpjpy, ohlc_eurusd, ohlc_gbpusd]:
    # for ohlc in [ohlc_usdjpy, ohlc_eurjpy, ohlc_gbpjpy]:
    for ohlc in [ohlc_usdjpy]:

        if ohlc.m1_updated == False:
            print (' ', ohlc.ticker, ':', '1minute', ' - ', ohlc.m1_updated)
            chart = ohlc.m1
            chart = indicator.add_sigma(chart, [20])
            chart = indicator.add_ema(chart, [5, 20, 60])
            chart = indicator.add_ema(chart, [25, 100, 300]) # 5分足の短期、中期、長期
            chart = indicator.add_ema(chart, [75, 300, 900]) # 15分足の短期、中期、長期
            chart = indicator.add_swing_high_low(chart)
            chart = indicator.add_ema_slope(chart, [5, 20, 60, 200])
            chart = indicator.add_bb(chart)
            chart = indicator.add_rci(chart)
            chart = indicator.add_ema_dr(chart)  
 
            chart = chart.tail(1000)
            chart_plot.plot_with_dr(f'html/{ohlc.ticker}_1minute.html', ohlc.ticker, chart)
        
        if ohlc.m5_updated == False:
            print (' ', ohlc.ticker, ':', '5minute', ' - ', ohlc.m5_updated)
            chart = ohlc.m5
            chart = indicator.add_sigma(chart, [20])
            chart = indicator.add_ema(chart, [5, 20, 60])
            chart = indicator.add_ema(chart, [4, 12]) # 1分足の中期、長期
            chart = indicator.add_ema(chart, [15, 60, 180]) # 15分足の短期、中期、長期
            chart = indicator.add_swing_high_low(chart)
            chart = indicator.add_ema_slope(chart, [5, 20, 60, 200])
            chart = indicator.add_bb(chart)
            chart = indicator.add_rci(chart)
            chart = indicator.add_ema_dr(chart)
            
            chart = chart.tail(500)
            # chart_plot.plot_with_dr(f'html/{ohlc.ticker}_5minute.html', ohlc.ticker, chart, min=5)
            chart_plot.plot_with_rci(f'html/{ohlc.ticker}_5minute.html', ohlc.ticker, chart)
            
        if ohlc.m15_updated == False:
            print (' ', ohlc.ticker, ':', '15minute', ' - ', ohlc.m15_updated)
            chart = ohlc.m15
            chart = indicator.add_ema(chart, [5, 20, 60])
            chart = indicator.add_ema(chart, [20, 80, 240]) # 1時間足の短期、中期、長期
            chart = indicator.add_ema(chart, [80, 320, 1160]) # 4時間足の短期、中期、長期
            chart = indicator.add_swing_high_low(chart)
            chart = indicator.add_ema_slope(chart, [5, 20, 60, 200])
            chart = indicator.add_bb(chart)
            chart = indicator.add_rci(chart)
            chart = indicator.add_ema_dr(chart)
            
            chart = chart.tail(700)
            # chart_plot.plot_for_simulation(f'html/{ohlc.ticker}_15minute.html', ohlc.ticker, chart)
            chart_plot.plot_with_rci(f'html/{ohlc.ticker}_15minute.html', ohlc.ticker, chart)
            
            
            
        if ohlc.h1_updated == False:
            print (' ', ohlc.ticker, ':', '60minute', ' - ', ohlc.h1_updated)
            chart = ohlc.h1
            chart = indicator.add_ema(chart,[5, 20, 60])
            chart = indicator.add_ema(chart, [20, 80, 240]) # 4時間足の短期、中期、長期
            chart = indicator.add_swing_high_low(chart)
            chart = indicator.add_ema_slope(chart, [5, 20, 60, 200])
            chart = indicator.add_bb(chart)
            chart = indicator.add_rci(chart)
            chart = indicator.add_ema_dr(chart)
            
            chart = chart.tail(700)
            chart_plot.plot_with_rci(f'html/{ohlc.ticker}_60minute.html', ohlc.ticker, chart)
            
            # 4時間足にリサンプリング
            ohlc_4h = ohlc.h1.resample('4h').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
            })
            ohlc_4h = ohlc_4h.dropna(subset=['Open', 'High', 'Low', 'Close'])
            
            ohlc_4h = indicator.add_ema(ohlc_4h,[5, 20, 60])
            ohlc_4h = indicator.add_swing_high_low(ohlc_4h)
            ohlc_4h = indicator.add_bb(ohlc_4h)
            ohlc_4h = indicator.add_rci(ohlc_4h)
            ohlc_4h = indicator.add_ema_dr(ohlc_4h)
            
            ohlc_4h = ohlc_4h.tail(1000)
            chart_plot.plot_with_rci(f'html/{ohlc.ticker}_240minute.html', ohlc.ticker, ohlc_4h)

        if ohlc.d1_updated == False:
            print (' ', ohlc.ticker, ':', '1day', ' - ', ohlc.m15_updated)
            chart = ohlc.d1
            chart = indicator.add_ema(chart, [5, 20, 60])
            chart = indicator.add_ema(chart, [20, 80, 240]) # 1時間足の短期、中期、長期
            chart = indicator.add_ema(chart, [80, 320, 1160]) # 4時間足の短期、中期、長期
            chart = indicator.add_swing_high_low(chart)
            chart = indicator.add_ema_slope(chart, [5, 20, 60, 200])
            chart = indicator.add_bb(chart)
            chart = indicator.add_rci(chart)
            chart = indicator.add_ema_dr(chart)
            
            chart = chart.tail(700)
            # chart_plot.plot_for_simulation(f'html/{ohlc.ticker}_15minute.html', ohlc.ticker, chart)
            chart_plot.plot_with_rci(f'html/{ohlc.ticker}_1day.html', ohlc.ticker, chart)
                
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
    
import yfinance
if __name__ == "__main__":
    
    os.system('cls')

    # pandasのprint表示の仕方を設定
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.width', 1000)
    
    analyze()

    # print(pandas.date_range('2023-07-01', '2023-07-31', freq='15T'))
 
 
            
