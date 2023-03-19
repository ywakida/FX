import pandas
import datetime
import os
import yfinance

# コンフィグ
# gdrivepath = '/content/drive/My Drive/stock/' # for google drive
basepath = './'
encode = 'utf-8'

# [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
def update_chart_csv(folder_path, ticker, interval):
    """ チャートのCSVの作成

    Args:
        folder_path (_type_): _description_
        ticker (_type_): _description_
    """
    file_name = f'{folder_path}/{ticker}_{interval}.csv'        
    if not os.path.exists(file_name):
        
        currency = yfinance.Ticker(f'{ticker}=X')
        new_chart = currency.history(period="max", interval=interval, progress=False)
        if not new_chart.empty: # 空データでない
            if len(new_chart) > 1: # ヘッダのみでない                
                new_chart.to_csv(file_name, header=True) # 保存
                print(f'{file_name} is created.')       
    
    else: 
        # csvファイルを読み取り、最新日付を取得する
        existed_chart =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
        
        print(existed_chart.index[-1].date())
        last_date = existed_chart.index[-1].date()
        # csvファイルの最新日付の翌日から本日までのデータを取得する
        today = datetime.date.today()
        print(today)
        delta_date = today - last_date
        delta_days = delta_date.days
        
        if delta_days <= 0:
            delta_days = 1
            
        delta_days = 1
        
        chart_diff = pandas.DataFrame()
        currency = yfinance.Ticker(f'{ticker}=X')
        
        chart_diff = currency.history(period=f'max', interval=interval, progress=False)            
        chart_diff.index = pandas.to_datetime(chart_diff.index)

        if not chart_diff.empty:
            if len(chart_diff) > 1:  
                
                chart = pandas.concat([chart, chart_diff])
                chart = chart[~chart.index.duplicated(keep='last')] # 重複があれば最新で更新する
                chart.sort_index(axis='index', ascending=True, inplace=True)
                chart.dropna(how='all', inplace=True)
                chart.to_csv(file_name, header=True) # 保存
                print(f"{file_name} is updated.")
               
        else:
            print(f'{file_name} is incorrect.')
        
def validate_chart_csv(folder_path, interval, ticker):
    """差分更新更新

    Args:
        folder_path (_type_): _description_
        ticker (_type_): _description_
    """
    file_name = f'{folder_path}/{ticker}_{interval}.csv'
    if os.path.exists(file_name):
        
        # csvファイルを読み取り、最新日付を取得する
        chart =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
        
        chart['timesatampdiff'] = chart.index.to_series().diff().dt.total_seconds() % 180000
        # chart['timesatampdiff'] = chart['timesatampdiff'] % 180000
        # chart['timesatampdiff'] = chart['timesatampdiff'].diff()
        
        
        print(chart['timesatampdiff'])
        

    else:
        print(f"{file_name} is not existed.")



def format_chart_csv(folder_path, interval, ticker):
    file_name = f'{folder_path}/{ticker}_{interval}.csv'
    if os.path.exists(file_name):
        
        # csvファイルを読み取り、最新日付を取得する
        chart =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
        
        # print(chart.tail(10)) 
        if (interval == '1h'):
            chart = chart.asfreq('1H')
        
        if (interval == '15m'):
            chart = chart.asfreq('15T')
    
        if (interval == '5m'):
            chart = chart.asfreq('5T')       
            
        # print(chart.tail(10)) 
        chart.to_csv(file_name, header=True) # 保存
        
def merge_chart_csv(folder_path_base, folder_path_add, folder_path_out, interval, currency):
    """差分更新更新

    Args:
        folder_path (_type_): _description_
        ticker (_type_): _description_
    """
    file_name1 = f'{folder_path_base}/{currency}_{interval}.csv'
    file_name2 = f'{folder_path_add}/{currency}_{interval}.csv'
    file_name3 = f'{folder_path_out}/{currency}_{interval}.csv'
    if os.path.exists(file_name1) and os.path.exists(file_name2):
        
        # csvファイルを読み取り、最新日付を取得する
        chart_base =  pandas.read_csv(file_name1, index_col=0, parse_dates=True)
        chart_add =  pandas.read_csv(file_name2, index_col=0, parse_dates=True)

        chart_base = pandas.concat([chart_base, chart_add])
        chart_base = chart_base[~chart_base.index.duplicated(keep='last')] # 重複があれば最新で更新する
        chart_base.sort_index(axis='index', ascending=True, inplace=True)
        if (interval == '1h'):
            chart_base = chart_base.asfreq('1H')
        
        if (interval == '15m'):
            chart_base = chart_base.asfreq('15T')
    
        if (interval == '5m'):
            chart_base = chart_base.asfreq('5T')
            
        chart_base.dropna(how='all', inplace=True)
        chart_base.reset_index(drop=True) # インデックスの降り直し　だけど、datetimeindexだから意味ないかも 
        chart_base.to_csv(file_name3, header=True) # 保存
        
        # chart_base.merge(chart_add)
        # chart_base = pandas.concat([chart_base, chart_add])
        # chart_base.reset_index(drop=True) # インデックスの降り直し　だけど、datetimeindexだから意味ないかも 
        # chart_base.drop_duplicates(keep='last', inplace=True) # 重複があれば最新で更新する
        # chart_base.to_csv(file_name3, header=True) # 保存
        print(f"{file_name3} is updated.")
        
    else:
        print(f"file is not existed.")
    
def task():
    folder = 'chart_csv'
    intervals = ['5m', '15m', '1h', '1d', '1wk']
    currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'NZDJPY', 'CADJPY', 'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'CADUSD']
    # intervals = ['5m']
    # currencies = ['USDJPY']
    
    for currency in currencies:
        print(currency, ":")
        
        for interval in intervals:
            print(" - ", interval)
            update_chart_csv(folder, currency, interval) 
            # format_chart_csv('_chart_csv', interval, currency)  
            # validate_chart_csv(folder, interval, currency)


if __name__ == "__main__":
    
    os.system('cls')

    # pandasのprint表示の仕方を設定
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.width', 1000)
    
    task()
        

 
 
            
