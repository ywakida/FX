import pandas
import datetime
import os
import yfinance
import time

# コンフィグ
# gdrivepath = '/content/drive/My Drive/stock/' # for google drive
basepath = './'
encode = 'utf-8'
folder = 'ohlc'
index_label = 'Datetime' # インデックスのラベル名
support_intervals = ['5m', '15m', '1h', '1d', '1wk']
support_periods = ['60d', '60d', '730d', 'max', 'max']
support_currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'NZDJPY', 'CADJPY', 'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'CADUSD']

class FxOhlc():
    
    def __init__(self, ticker, debug=False):
        self.debug = debug
        self.m5 = pandas.DataFrame()
        self.m15 = pandas.DataFrame()
        self.h1 = pandas.DataFrame()
        
        self.ticker = ''
        if ticker in support_currencies:
            self.ticker = ticker
            
            self.m5 = self.__load(self.ticker, '5m')
            self.m15 = self.__load(self.ticker, '15m')
        
        else:
            raise ValueError(ticker, ' is incorrected.')      
        
    def __load(self, ticker, interaval):
        chart = pandas.DataFrame()
        
        file_name = f'{folder}/{ticker}_{interaval}.csv'
        if os.path.exists(file_name):
            chart =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
            chart.index = pandas.to_datetime(chart.index, utc=True)
            chart.index.name = index_label # インデックスラベル名を作成
            
            if self.debug:
                print(len(chart), ' row data is loaded.')
                pass
        else:
            raise NameError(file_name, 'is not found.')
        
        return chart

        
    def __append_online_data(self, chart, interval):
        
        currency = yfinance.Ticker(f'{self.ticker}=X')
        append_chart = currency.history(interval=interval, start=chart.index[-1].date())
        # append_chart = currency.history(interval='5m', period='1d')
        append_chart.index = pandas.to_datetime(append_chart.index, utc=True)
        append_chart = append_chart[['Open', 'High', 'Low', 'Close']] # 不要な列を削除する
        append_chart.index.name = index_label # インデックスラベル名を作成
        append_chart = append_chart[:-1] # 末尾を削除
                
        if not append_chart.empty:
            if len(append_chart) > 1:
                chart = pandas.concat([chart, append_chart])
                chart = chart[~chart.index.duplicated(keep='last')] # 重複があれば最新で更新する
                chart.sort_index(axis='index', ascending=True, inplace=True)
                chart.dropna(how='all', inplace=True)
                chart.index.name = 'Datetime' # インデックスラベル名を作成

        return chart

    def append_online_data(self):
        self.m5 = self.__append_online_data(self.m5, '5m')
        self.m15 = self.__append_online_data(self.m15, '15m')
        
        
def load_stored_data(ticker, interval):
    """ 保存してあるデータをロードする
    """
    chart = pandas.DataFrame()
    if ticker in support_currencies and interval in support_intervals:
        file_name = f'{folder}/{ticker}_{interval}.csv'
        if os.path.exists(file_name):
            chart =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
            chart.index = pandas.to_datetime(chart.index, utc=True)
            chart.index.name = index_label # インデックスラベル名を作成
        else:
            raise NameError(file_name, 'is not found.')
    else:
        raise ValueError('argument is incorrected.')
        
    return chart

def get_online_data(ticker, interval, period):
    
    chart = pandas.DataFrame()
    if ticker in support_currencies and interval in support_intervals:# and period in support_periods:      
        currency = yfinance.Ticker(f'{ticker}=X')
        chart = currency.history(period=period, interval=interval)
        chart.index = pandas.to_datetime(chart.index, utc=True)
        chart = chart[['Open', 'High', 'Low', 'Close']] # 不要な列を削除する
        chart.index.name = index_label # インデックスラベル名を作成
    else:
        raise ValueError('argument is incorrected.')

    return chart
    
def append_online_data(chart, ticker, interval, period):
    
    append_chart = get_online_data(ticker, interval, period)
    
    if not append_chart.empty:
        if len(append_chart) > 1:
            chart = pandas.concat([chart, append_chart])
            chart = chart[~chart.index.duplicated(keep='last')] # 重複があれば最新で更新する
            chart.sort_index(axis='index', ascending=True, inplace=True)
            chart.dropna(how='all', inplace=True)
            chart.index.name = 'Datetime' # インデックスラベル名を作成

    return chart
        
# [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
def update_chart_csv(folder_path, ticker, interval, period, is_save=True):
    """ チャートのCSVの作成

    Args:
        folder_path (_type_): _description_
        ticker (_type_): _description_
    """
    file_name = f'{folder_path}/{ticker}_{interval}.csv'        
    if not os.path.exists(file_name):
        
        currency = yfinance.Ticker(f'{ticker}=X')
        new_chart = currency.history(periods='max', interval=interval)
        if not new_chart.empty: # 空データでない
            if len(new_chart) > 1: # ヘッダのみでない
                if is_save == True:
                    new_chart.index.name = 'Datetime' # インデックスラベル名を作成
                    new_chart = new_chart[['Open', 'High', 'Low', 'Close']] # 不要な列を削除する
                    new_chart.to_csv(file_name, header=True) # 保存
                    print(f'{file_name} is created.')       
    
    else: 
        # csvファイルを読み取り、最新日付を取得する
        existed_chart =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
        existed_chart.index = pandas.to_datetime(existed_chart.index, utc=True)
        
        # print(existed_chart.head(10))
        print("recorded last date: ", existed_chart.index[-1].date())
        last_date = existed_chart.index[-1].date()
        # csvファイルの最新日付の翌日から本日までのデータを取得する
        today = datetime.date.today()
        print("today's date: ", today)
        delta_date = today - last_date
        delta_days = delta_date.days
        
        if delta_days <= 0:
            delta_days = 1
            
        delta_days = 1
        
        chart_diff = pandas.DataFrame()
        currency = yfinance.Ticker(f'{ticker}=X')
        chart_diff = currency.history(period=period, interval=interval)            
        chart_diff.index = pandas.to_datetime(chart_diff.index, utc=True)
        chart_diff = chart_diff[['Open', 'High', 'Low', 'Close']] # 不要な列を削除する
        chart_diff.index.name = 'Datetime' # インデックスラベル名を作成
        print("update length: ", len(chart_diff))
        chart_diff = chart_diff[:-1] # 末尾1行を削除
        

        if not chart_diff.empty:
            if len(chart_diff) > 1:  
                
                chart = pandas.concat([existed_chart, chart_diff])
                chart = chart[~chart.index.duplicated(keep='last')] # 重複があれば最新で更新する
                chart.sort_index(axis='index', ascending=True, inplace=True)
                chart.dropna(how='all', inplace=True)
                # print(chart.head(10))
                chart.index.name = 'Datetime' # インデックスラベル名を作成
                
                if is_save == True:  
                    chart.to_csv(file_name, header=True) # 保存
                    print(f"{file_name} is updated.")
               
        else:
            print(f'{file_name} is incorrect.')
        
def save_ohlc():
    intervals = ['5m', '15m', '1h', '1d', '1wk']
    periods = ['60d', '60d', '730d', 'max', 'max']
    currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'NZDJPY', 'CADJPY', 'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'CADUSD']
    # intervals = ['5m']
    # currencies = ['USDJPY']
    
    for currency in currencies:
        print(currency, ":")
        
        for interval, period in zip(intervals, periods):
            print(" - ", interval, ":", period)
            update_chart_csv(folder, currency, interval, period, True) 
            
def add_index():
    intervals = ['5m', '15m', '1h', '1d', '1wk']
    currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'NZDJPY', 'CADJPY', 'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'CADUSD']
    
    for currency in currencies:
        print(currency, ":")
        
        for interval in intervals:
            print(" - ", interval)
            
            file_name = f'{folder}/{currency}_{interval}.csv'
            if os.path.exists(file_name):
                existed_chart =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
                existed_chart.index = pandas.to_datetime(existed_chart.index, utc=True)
                
                existed_chart.index.name = 'Datetime'
                print(existed_chart.index.name)
                existed_chart.to_csv(file_name, header=True) 
            
def remove_columns():
    intervals = ['5m', '15m', '1h', '1d', '1wk']
    currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'NZDJPY', 'CADJPY', 'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'CADUSD']
    
    for currency in currencies:
        print(currency, ":")
        
        for interval in intervals:
            print(" - ", interval)
            
            file_name = f'{folder}/{currency}_{interval}.csv'
            if os.path.exists(file_name):
                existed_chart =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
                existed_chart.index = pandas.to_datetime(existed_chart.index, utc=True)
                
                existed_chart = existed_chart[['Open', 'High', 'Low', 'Close']]
                existed_chart.to_csv(file_name, header=True) 
                


def task2():
    intervals = ['1m', '5m', '15m', '1h']
    periods = ['7d', '60d', '60d', '730d']
    currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'EURUSD', 'GBPUSD']
    intervals = ['5m']
    periods = ['1d']
    currencies = ['USDJPY']
    
    for currency in currencies:
        print(currency, ":")
        
        for interval, period in zip(intervals, periods):
            print(" - ", interval, ":", period)
            get_online_data(currency, interval, period)

if __name__ == "__main__":
    
    os.system('cls')

    # pandasのprint表示の仕方を設定
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.width', 1000)
    
    # task()
    # remove_columns()

    currency = 'USDJPY'    
    interval = '5m'
    period = '2d'
    
    ohlc = FxOhlc(currency, True)
    
    print(ohlc.m15.index[-1])
    
    ohlc.append_online_data()

    # time.sleep(10)
    # print(ohlc.m15.index[-1])
    # ohlc.append_online_data()

    # time.sleep(10)
    # print(ohlc.m15.index[-1])
    # ohlc.append_online_data()
    # time.sleep(10)
    # print(ohlc.m15.index[-1])
    # ohlc.append_online_data()
    # time.sleep(10)
    # print(ohlc.m15.index[-1])
    # ohlc.append_online_data()
    # time.sleep(10)
    # print(ohlc.m15.index[-1])
    # ohlc.append_online_data()
    

    
    # chart = load_stored_data(currency, interval)
    # chart = get_online_data(currency, interval, period)
    # chart = chart.head(10)
    # print(chart)
    # chart = append_online_data(chart, currency, interval, '1d')
    # print(chart)
    
        

 
 
            
