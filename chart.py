import pandas
import datetime
import os
import yfinance

# コンフィグ
# gdrivepath = '/content/drive/My Drive/stock/' # for google drive
basepath = './'
encode = 'utf-8'

# [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
def update_chart_csv(folder_path, ticker, interval, is_save=True):
    """ チャートのCSVの作成

    Args:
        folder_path (_type_): _description_
        ticker (_type_): _description_
    """
    file_name = f'{folder_path}/{ticker}_{interval}.csv'        
    if not os.path.exists(file_name):
        
        currency = yfinance.Ticker(f'{ticker}=X')
        new_chart = currency.history(periods="max", interval=interval, progress=False)
        if not new_chart.empty: # 空データでない
            if len(new_chart) > 1: # ヘッダのみでない
                if is_save == True:    
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
        
        chart_diff = currency.history(periods=f'max', interval=interval, progress=False)            
        chart_diff.index = pandas.to_datetime(chart_diff.index)
        
        chart_diff = chart_diff[:-1] # 末尾1行を削除

        if not chart_diff.empty:
            if len(chart_diff) > 1:  
                
                chart = pandas.concat([existed_chart, chart_diff])
                chart = chart[~chart.index.duplicated(keep='last')] # 重複があれば最新で更新する
                chart.sort_index(axis='index', ascending=True, inplace=True)
                chart.dropna(how='all', inplace=True)
                
                print(chart.tail(10))
                
                # latest_date = chart.index[-1]                
                # print(latest_date)
                # print(latest_date.second)
                # print(latest_date.minute)
                
                
                if is_save == True:  
                    chart.to_csv(file_name, header=True) # 保存
                    print(f"{file_name} is updated.")
               
        else:
            print(f'{file_name} is incorrect.')
        
def task():
    folder = 'chart_csv'
    intervals = ['5m', '15m', '1h', '1d', '1wk']
    currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'NZDJPY', 'CADJPY', 'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'CADUSD']
    
    for currency in currencies:
        print(currency, ":")
        
        for interval in intervals:
            print(" - ", interval)
            update_chart_csv(folder, currency, interval) 


if __name__ == "__main__":
    
    os.system('cls')

    # pandasのprint表示の仕方を設定
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.width', 1000)
    
    task()
        

 
 
            
