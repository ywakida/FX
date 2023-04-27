import pandas
import datetime
import os
import chart
import indicator

# コンフィグ
# gdrivepath = '/content/drive/My Drive/stock/' # for google drive
basepath = './'
encode = 'utf-8'
folder = 'ohlc'

        
def analyze():
    intervals = ['5m', '15m', '1h', '1d', '1wk']
    periods = ['60d', '60d', '730d', 'max', 'max']
    currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'NZDJPY', 'CADJPY', 'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'CADUSD']
    intervals = ['5m']
    currencies = ['USDJPY']
    
    for currency in currencies:
        print(currency, ":")
        
        for interval, period in zip(intervals, periods):
            print(" - ", interval, ":", period)
            
            ohlc = chart.get_chart(currency, interval, period) 
            
            print(ohlc)


if __name__ == "__main__":
    
    os.system('cls')

    # pandasのprint表示の仕方を設定
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.width', 1000)
        
    analyze()
        

 
 
            
