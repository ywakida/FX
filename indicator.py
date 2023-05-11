import pandas
import datetime
import math
import os
import numpy

def add_sma(chart, params=[5, 20, 60]):
    """ 単純移動平均線の追加
    """
    for param in params:
        if not f'SMA{param}' in chart.columns:
            chart[f'SMA{param}'] = chart['Close'].rolling(param).mean() 
            
    return chart

def add_sma_dr(chart, params=[5, 20, 60]):
    """ 単純移動平均線からの乖離率(%)
    """
    for param in params:
        if f'SMA{param}' in chart.columns:
            chart[f'SMADR{param}']   = (chart['Close'] - chart[f'SMA{param}']) / chart[f'SMA{param}'] * 100
            
    return chart
        
def add_sma_slope(chart, params=[20], base=1000):
    """ シグマ
    """     
    for param in params:
        chart[f'Slope{param}'] = chart[f'SMA{param}'].diff() * base
    
    return chart
            
def add_ema(chart, params=[5, 20, 60]):
    """ 指数移動平均線の追加
    """
    for param in params:
        if not f'EMA{param}' in chart.columns:
            chart[f'EMA{param}'] = chart['Close'].ewm(span=param, adjust=False).mean()
    
    return chart
        
def add_ema_dr(chart, params=[5, 20, 60]):
    """ 指数移動平均線からの乖離率(%)
    """
    for param in params:
        if f'EMA{param}' in chart.columns:
            chart[f'EMADR{param}']   = (chart['Close'] - chart[f'EMA{param}']) / chart[f'EMA{param}'] * 100

    return chart

def add_ema_slope(chart, params=[20], base=1000):
    """ シグマ
    """     
    for param in params:
        chart[f'Slope{param}'] = chart[f'EMA{param}'].diff() * base

    return chart

def add_bb(chart, params=[5, 20, 60]):
    """ ボリンジャーバンド
    """
    for param in params:
        chart[f'BB{param}P2'] = chart['Close'].rolling(param).mean() + 2 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団
        chart[f'BB{param}P1'] = chart['Close'].rolling(param).mean() + 1 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団
        chart[f'BB{param}M1'] = chart['Close'].rolling(param).mean() - 1 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団
        chart[f'BB{param}M2'] = chart['Close'].rolling(param).mean() - 2 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団
    
    return chart

def add_sigma(chart, params=[20]):
    """ シグマ
    """     
    for param in params:
        chart[f'SIGMA{param}'] = (chart['Close'] - chart['Close'].rolling(param).mean()) / chart['Close'].rolling(param).std(ddof = 0)  # ddof = 0は母集団 
        chart[f'SIGMA{param}'].mask((chart[f'SIGMA{param}'] >= 0), (chart['High'] - chart['Close'].rolling(param).mean()) / chart['Close'].rolling(param).std(ddof = 0), inplace=True)
        chart[f'SIGMA{param}'].mask((chart[f'SIGMA{param}'] < 0), (chart['Low'] - chart['Close'].rolling(param).mean()) / chart['Close'].rolling(param).std(ddof = 0), inplace=True)
        # chart[f'SIGMA{param}'] = chart[f'SIGMA{param}'].ewm(span=5, adjust=False).mean()
    
    return chart 
    
def add_basic(chart, params=[5, 20, 60, 200]):
    """ 基本インジケータの追加
    """
    for param in params:
        # 単純移動平均 Simple moving average
        chart[f'SMA{param}'] = chart['Close'].rolling(param).mean()
        
        # 乖離率 Deviation rate
        chart[f'DR{param}']   = (chart['Close'] - chart[f'SMA{param}']) / chart[f'SMA{param}'] * 100
       
        # 前日からの傾き
        chart[f'Slope{param}'] = chart[f'SMA{param}'].pct_change(1)
        
        # 傾き変化量
        chart[f'SlopeSlope{param}'] = chart[f'Slope{param}'].pct_change(1)
        
        # 指数移動平均
        chart[f'EMA{param}'] = chart['Close'].ewm(span=param, adjust=False).mean()
                
        # ボリンジャーバンド
        chart[f'BB{param}P2'] = chart['Close'].rolling(param).mean() + 2 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団
        chart[f'BB{param}P1'] = chart['Close'].rolling(param).mean() + 1 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団
        chart[f'BB{param}M1'] = chart['Close'].rolling(param).mean() - 1 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団
        chart[f'BB{param}M2'] = chart['Close'].rolling(param).mean() - 2 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団
        
        # 変則シグマ
        chart[f'SIGMA{param}'] = (chart['Close'] - chart['Close'].rolling(param).mean()) / chart['Close'].rolling(param).std(ddof = 0)  # ddof = 0は母集団
        chart[f'SIGMA{param}'].mask((chart[f'SIGMA{param}'] > 0), (chart['High'] - chart['Close'].rolling(param).mean()) / chart['Close'].rolling(param).std(ddof = 0), inplace=True)
        chart[f'SIGMA{param}'].mask((chart[f'SIGMA{param}'] < 0), (chart['Low'] - chart['Close'].rolling(param).mean()) / chart['Close'].rolling(param).std(ddof = 0), inplace=True)
        # chart[f'SIGMA{param}'] = chart[f'SIGMA{param}'].ewm(span=5, adjust=False).mean()


def calc_rci(prices):
    """ RCI 計算関数
    """
    day_cnt = len(prices)
    # 日付昇順ランク
    rank_day = numpy.arange(day_cnt) + 1
    # 株価昇順ランク
    rank_price = numpy.array(pandas.Series(prices).rank())
    rci = 1 - (6 * ((rank_day - rank_price)**2).sum()) / (day_cnt * (day_cnt**2 - 1))
    return rci * 100 # パーセント値で返却

def add_rci(chart, days=9):
    """ RCIの追加
    """        
    chart['Rci'] = chart['Close'].rolling(days).apply(calc_rci, raw=True)

    return chart

def add_heikinashi(chart):
    """平均足の追加

    Args:
        chart (_type_): _description_
    """
    diff = 0.5
    # chart['HA_Close'] = (chart['High'] + chart['Low'] + chart['Open'] + chart['Close']) / 4 - diff
    # chart['HA_Open'] = (chart['Open'] + chart['Close']) / 2 - diff
    # chart['HA_Open'] = chart['HA_Open'].shift(1) # 前回の値に変更
    # chart['HA_High'] = chart['High'] - diff
    # chart['HA_Low'] = chart['Low'] - diff
    # chart['HA_High'] = pandas.concat([chart['HA_Open'], chart['HA_Close'], chart['High']], axis='columns').max(axis='columns')
    # chart['HA_Low'] = pandas.concat([chart['HA_Open'], chart['HA_Close'], chart['Low']], axis='columns').min(axis='columns')
    
    param = 3
    ad = True
    chart['HA_Close'] = (chart['High'].ewm(span=param, adjust=ad).mean() + chart['Low'].ewm(span=param, adjust=ad).mean() + chart['Open'].ewm(span=param, adjust=ad).mean() + chart['Close'].ewm(span=param, adjust=ad).mean()) / 4 - diff
    chart['HA_Open'] = (chart['Open'].ewm(span=param, adjust=ad).mean() + chart['Close'].ewm(span=param, adjust=ad).mean()) / 2
    chart['HA_Open'] = chart['HA_Open'].shift(1) - diff # 前回の値に変更
    chart['HA_High'] = chart['High'] - diff
    chart['HA_Low'] = chart['Low'] - diff
    # chart['HA_High'] = pandas.concat([chart['HA_Open'], chart['HA_Close'], chart['High']], axis='columns').max(axis='columns')
    # chart['HA_Low'] = pandas.concat([chart['HA_Open'], chart['HA_Close'], chart['Low']], axis='columns').min(axis='columns')
    
    
    # 平均足の陽線と陰線の反転
    chart['HA_Reversal_Plus'] = (chart['HA_Close'] > chart['HA_Open']) & (chart['HA_Close'] < chart['HA_Open']).shift(1)
    chart['HA_Reversal_Minus'] = (chart['HA_Close'] < chart['HA_Open']) & (chart['HA_Close'] > chart['HA_Open']).shift(1)
    
    # 陽線が1, 陰線が-1
    chart['HA_3V'] = 0
    chart['HA_3V'].mask((chart['HA_Close'] > chart['HA_Open']), 1, inplace=True)
    chart['HA_3V'].mask((chart['HA_Close'] < chart['HA_Open']), -1, inplace=True)

    return chart

def add_swing_high_low(chart, width=5):
    """スイングハイ、ローの検出
    """
    window=width * 2 + 1
    chart[f'SwingHigh'] = 0
    chart[f'SwingHigh'].mask((chart['High'].rolling(window, center=True).max() == chart['High']), chart['High'], inplace=True)
    chart[f'SwingLow'] = 0
    chart[f'SwingLow'].mask((chart['Low'].rolling(window, center=True).min() == chart['Low']), chart['Low'], inplace=True)

    return chart

def add_before(chart, day=1):
    """X日前の値

    Args:
        chart (_type_): チャート
        day (int, optional): day. Defaults to 1.
    """
    chart[f'OpenBefore{day}'] = chart['Open'].shift(day)
    chart[f'HighBefore{day}'] = chart['High'].shift(day)
    chart[f'LowBefore{day}'] = chart['Low'].shift(day)
    chart[f'CloseBefore{day}'] = chart['Close'].shift(day)






def analize_sma(chart, currency):
    
    # トレンド転換の可能性のある5MA, 20MA, 60MA突き抜け
    chart['BreakPlus'] = (chart['Close']>chart['Open'])&(chart['Close']>chart['SMA60'])&(chart['Close']>chart['SMA20'])&(chart['Close']>chart['SMA5'])
    # chart['BreakPlus'] = (chart['Close']>chart['Open'])&(chart['Close']>chart['SMA20'])&(chart['Close']>chart['SMA5'])
    chart['BreakPlus'] = (chart['BreakPlus'] == True) & (chart['BreakPlus'].shift(1) == False)
    chart['BreakMinus'] = (chart['Close']<chart['Open'])&(chart['Close']<chart['SMA60'])&(chart['Close']<chart['SMA20'])&(chart['Close']<chart['SMA5'])
    # chart['BreakMinus'] = (chart['Close']<chart['Open'])&(chart['Close']<chart['SMA20'])&(chart['Close']<chart['SMA5'])
    chart['BreakMinus'] = (chart['BreakMinus'] == True) & (chart['BreakMinus'].shift(1) == False)
     


def analize(chart, currency):
    """解析

    Args:
        file_name (_type_): _description_
        currency (_type_): _description_

    Returns:
        _type_: _description_
    """
    # open chart csv file
    # chart =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
    # print(daily_chart)
    
    params = [5, 20, 60, 240]
    
    for param in params:
        # 単純移動平均 Simple moving average
        chart[f'SMA{param}'] = chart['Close'].rolling(param).mean() # 5分足の短期移動平均
        # chart[f'SMA{param}'].fillna(method='bfill', inplace=True)
        
        # 乖離率 Deviation rate
        chart[f'DR{param}']   = (chart['Close'] - chart[f'SMA{param}']) / chart[f'SMA{param}'] * 100
       
        # 前日からの傾き
        chart[f'Slope{param}'] = chart[f'SMA{param}'].pct_change(1)
        
        # 傾き変化量
        chart[f'SlopeSlope{param}'] = chart[f'Slope{param}'].pct_change(1)
        
        # 指数移動平均
        chart[f'EMA{param}'] = chart['Close'].ewm(span=param, adjust=False).mean()
        
        # ボリンジャーバンド
        chart[f'BB{param}P2'] = chart['Close'].rolling(param).mean() + 2 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団
        chart[f'BB{param}P1'] = chart['Close'].rolling(param).mean() + 1 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団
        chart[f'BB{param}M1'] = chart['Close'].rolling(param).mean() - 1 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団
        chart[f'BB{param}M2'] = chart['Close'].rolling(param).mean() - 2 * chart['Close'].rolling(param).std(ddof = 0) # ddof = 0は母集団

    
    # 直近高値、直近安値の計算
    add_swing_high_low(chart)
    
    # トレンド転換の可能性のある5MA, 20MA, 60MA突き抜け
    chart['BreakPlus'] = (chart['Close']>chart['Open'])&(chart['Close']>chart['SMA60'])&(chart['Close']>chart['SMA20'])&(chart['Close']>chart['SMA5'])
    # chart['BreakPlus'] = (chart['Close']>chart['Open'])&(chart['Close']>chart['SMA20'])&(chart['Close']>chart['SMA5'])
    chart['BreakPlus'] = (chart['BreakPlus'] == True) & (chart['BreakPlus'].shift(1) == False)
    chart['BreakMinus'] = (chart['Close']<chart['Open'])&(chart['Close']<chart['SMA60'])&(chart['Close']<chart['SMA20'])&(chart['Close']<chart['SMA5'])
    # chart['BreakMinus'] = (chart['Close']<chart['Open'])&(chart['Close']<chart['SMA20'])&(chart['Close']<chart['SMA5'])
    chart['BreakMinus'] = (chart['BreakMinus'] == True) & (chart['BreakMinus'].shift(1) == False)
     

    # # 下半身上昇
    # # ・陽線であること
    # # ・5日移動平均を半分以上上であること
    # # ・傾きが平行もしくは上昇に転じたところであること
    # # ・前日が5日移動平均線の下にあり、突き抜けること
    # chart['Kahanshin'] = 0
    # chart['Kahanshin'].mask((chart["Close"]>chart["Open"])&((chart["Close"]+chart["Open"])/2>=chart["SMA5"])&(chart["Slope5"]>=-0.5), 1, inplace=True)
    # chart['Kahanshin'] = chart['Kahanshin'].diff()
    
       
    return chart

    
    # # 平行度        
    # daily_chart['Parallel'] = daily_chart['Slope25'] - daily_chart['Slope75']
    
    
    # daily_chart['PerfectOrder'] = 0
    # daily_chart['PerfectOrder'].mask((daily_chart['SMA5'] >= daily_chart['SMA25'])&(daily_chart['SMA25'] >= daily_chart['SMA75'])&(daily_chart['Slope25'] >= 0.0)&(daily_chart['Slope75'] < 0.0), 1, inplace=True)
    # daily_chart['PerfectOrder'].mask((daily_chart['SMA5'] >= daily_chart['SMA25'])&(daily_chart['SMA25'] >= daily_chart['SMA75'])&(daily_chart['Slope25'] >= 0.0)&(daily_chart['Slope75'] >= 0.0), 2, inplace=True)
    # daily_chart['PerfectOrder'].mask((daily_chart['SMA5'] >= daily_chart['SMA25'])&(daily_chart['SMA25'] >= daily_chart['SMA75'])&(daily_chart['Slope25'] >= 0.0)&(daily_chart['Slope75'] >= 0.0)&(daily_chart['Slope5'] >= 0.0), 3, inplace=True)

    # daily_chart['PPP'] = 0
    # daily_chart['PPP'].mask((daily_chart['SMA5'] >= daily_chart['SMA20'])&(daily_chart['SMA20'] >= daily_chart['SMA60'])&(daily_chart['SMA60'] >= daily_chart['SMA100']), 1, inplace=True)
    
    # # daily_chart['Perfect2'] = 0
    # # daily_chart['Perfect2'].mask((daily_chart['Slope5'] > 0.0) & (daily_chart['Slope25'] > 0.0 ) & (daily_chart['SMA75'] >= daily_chart['Slope60']), 3, inplace=True)
    # # daily_chart['Perfect2'].mask((daily_chart['Slope5'] <= 0.0) & (daily_chart['Slope25'] > 0.0 ) & (daily_chart['SMA75'] >= daily_chart['Slope60']), 2, inplace=True)
    # # daily_chart['Perfect2'].mask((daily_chart['Slope5'] <= 0.0) & (daily_chart['Slope25'] <= 0.0 ) & (daily_chart['SMA75'] >= daily_chart['Slope60']), 1, inplace=True)
    
    # # 下落率
    # daily_chart['Drop5'] = 0
    # daily_chart['Drop5'].mask(daily_chart['High'].rolling(5).max() > daily_chart['Close'], (daily_chart['High'].rolling(5).max() - daily_chart['Close']) / daily_chart['High'].rolling(5).max() * 100, inplace=True)
    
    # # 乖離率が何シグマかの判定
    # # 乖離率は、一定以上のデータがないと判定しないようにする
    # # まだ株ちゃんのノウハウに従って、25MAの場合は、2000本以上のデータが必要とした
    # if len(daily_chart) >= 200:
    #     mean = daily_chart['DR5'].mean()
    #     std = daily_chart['DR5'].std()
    #     daily_chart['SIGMA5'] = (daily_chart['DR5'] - mean) / std
    # else:
    #     daily_chart['SIGMA5'] = 0
        
    # if len(daily_chart) >= 1000:
    #     mean = daily_chart['DR20'].mean()
    #     std = daily_chart['DR20'].std()
    #     daily_chart['SIGMA20'] = (daily_chart['DR20'] - mean) / std
    #     # mean = daily_chart['DR25'].mean()
    #     # std = daily_chart['DR25'].std()
    #     # daily_chart['SIGMA25'] = (daily_chart['DR25'] - mean) / std
    # else:
    #     daily_chart['SIGMA20'] = 0
    #     # daily_chart['SIGMA25'] = 0
    
    # # 暴落
    # daily_chart['Boraku'] = 0
    # daily_chart['Boraku'].mask((daily_chart["SIGMA5"]<-1.0)&(daily_chart["Low"]>daily_chart["SMA75"])&(daily_chart["PerfectOrder"]>=2), 1, inplace=True)
    # daily_chart['Boraku'].mask((daily_chart["SIGMA5"]<-1.5)&(daily_chart["Low"]>daily_chart["SMA75"])&(daily_chart["PerfectOrder"]>=2), 2, inplace=True)
    # daily_chart['Boraku'].mask((daily_chart["SIGMA5"]<-2.0)&(daily_chart["Low"]>daily_chart["SMA75"])&(daily_chart["PerfectOrder"]>=2), 3, inplace=True)
    # daily_chart['Boraku'].mask((daily_chart["SIGMA5"]<-2.5)&(daily_chart["Low"]>daily_chart["SMA75"])&(daily_chart["PerfectOrder"]>=2), 4, inplace=True)
    # daily_chart['Boraku'].mask((daily_chart["SIGMA5"]<-3.0)&(daily_chart["Low"]>daily_chart["SMA75"])&(daily_chart["PerfectOrder"]>=2), 5, inplace=True)
    
    # # csv 保存
    # save_folder_path = './metrics/'
    # daily_chart.to_csv(save_folder_path + f'{ticker}.csv')
    
    # # print(daily_chart.tail(10))    
    # print(daily_chart.head(200))
    # # mplfinance_show(ticker, daily_chart)
    # save_folder_path = './html/'
    # figure = plotly_show(save_folder_path, ticker, row['銘柄名'], daily_chart.tail(200))
    
    
    # date_path = pandas.to_datetime(daily_chart.tail(1).index.date[0]).date().strftime('%Y%m%d')
    # # figure.write_image(f'{ticker}.png')
    # # print(date_path)
    # os.makedirs(str(date_path), exist_ok=True)
    
    # if daily_chart.iloc[-1]['Boraku'] >= 1:
        
    #     os.makedirs(str(date_path) + '/Boraku', exist_ok=True)
    #     print(f'{ticker}:' ,daily_chart.iloc[-1]['SIGMA5'], ' ', daily_chart.iloc[-1]['DR5'])
        
    #     # PNG, JPEG, SVG, PDF
    #     # figure.write_image(f'{date_path}/{ticker}.png')
    #     figure = plotly_show(f'{date_path}/Boraku/', ticker, row['銘柄名'], daily_chart.tail(100))
    #     filename = f'{date_path}/Boraku/boraku.csv'

    #     df_out = pandas.DataFrame(index=[ticker])
    #     df_out['sigma_5days'] = daily_chart.iloc[-1]['SIGMA5']
    #     df_out['dr_5days'] = daily_chart.iloc[-1]['DR5']
    #     df_out['SMA5'] = daily_chart.iloc[-1]['SMA5']
    #     df_out['SMA25'] = daily_chart.iloc[-1]['SMA25']
    #     df_out['SMA75'] = daily_chart.iloc[-1]['SMA75']
    #     df_out['PPP'] = daily_chart.iloc[-1]['PPP']
    #     df_out['dr5_10%'] = math.ceil(daily_chart.iloc[-1]['SMA5'] - daily_chart.iloc[-1]['SMA5'] * 0.10)
    #     df_out['dr5_15%'] = math.ceil(daily_chart.iloc[-1]['SMA5'] - daily_chart.iloc[-1]['SMA5'] * 0.15)
    #     df_out['dr5_20%'] = math.ceil(daily_chart.iloc[-1]['SMA5'] - daily_chart.iloc[-1]['SMA5'] * 0.2)
    #     df_out['dr5_25%'] = math.ceil(daily_chart.iloc[-1]['SMA5'] - daily_chart.iloc[-1]['SMA5'] * 0.25)
    #     df_out['dr5_30%'] = math.ceil(daily_chart.iloc[-1]['SMA5'] - daily_chart.iloc[-1]['SMA5'] * 0.3)
    #     if not os.path.exists(filename):
    #         df_out.to_csv(filename, mode='w', header=True)
    #     else:
    #         df_out.to_csv(filename, mode='a', header=False)

    # if daily_chart.iloc[-1]['Kahanshin'] >= 1:
    #     os.makedirs(str(date_path) + '/Kahanshin', exist_ok=True)                
    #     # PNG, JPEG, SVG, PDF
    #     # figure.write_image(f'{date_path}/{ticker}.png')
    #     figure = plotly_show(f'{date_path}/kahanshin/', ticker, row['銘柄名'], daily_chart.tail(100))
    #     filename = f'{date_path}/kahanshin/kahanshin.csv'
    #     print(f'{ticker}:' ,daily_chart.iloc[-1]['SIGMA5'], ' ', daily_chart.iloc[-1]['DR5'])
    #     df_out = pandas.DataFrame(index=[ticker])
    #     df_out['Close'] = daily_chart.iloc[-1]['Close']
    #     df_out['SMA5'] = daily_chart.iloc[-1]['SMA5']
    #     df_out['SMA20'] = daily_chart.iloc[-1]['SMA20']
    #     df_out['SMA60'] = daily_chart.iloc[-1]['SMA60']
    #     df_out['SMA100'] = daily_chart.iloc[-1]['SMA100']
    #     df_out['Slope5'] = daily_chart.iloc[-1]['Slope5']
    #     df_out['Slope20'] = daily_chart.iloc[-1]['Slope20']
    #     df_out['Slope60'] = daily_chart.iloc[-1]['Slope60']
    #     df_out['PerfectOrder'] = daily_chart.iloc[-1]['PerfectOrder']
    #     df_out['PPP'] = daily_chart.iloc[-1]['PPP']
        
    #     if not os.path.exists(filename):
    #         df_out.to_csv(filename, mode='w', header=True)
    #     else:
    #         df_out.to_csv(filename, mode='a', header=False)

def analize_multi(currency):
    timeframes = ['5m', '15m', '1h']
    for timeframe in timeframes:
        file_name = f'_chart_csv/{currency}_{timeframe}.csv'
        if os.path.exists(file_name):
            chart_5m = analize(file_name, currency)
            # print(chart.head(100))
            # print (chart.loc[:,['High', 'SwingHigh']])
            # print(chart['HA_Reversal_flag'])
            save_folder_path = '_html'
            # figure = plotly_show(save_folder_path, currency, chart_5m.tail(100), False)
             

if __name__ == "__main__":
    
    os.system('cls')

    # pandasのprint表示の仕方を設定
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.width', 1000)
    
    # currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'EURUSD', 'GBPUSD', 'AUDUSD']
    currencies = ['USDJPY']
    for currency in currencies:
        file_name = f'chart_csv/{currency}_5m.csv'
        if os.path.exists(file_name):
            
            chart_5m =  pandas.read_csv(file_name, index_col=0, parse_dates=True)

            add_basic(chart_5m, [5, 20, 60, 200, 15, 180, ])
            
            add_heikinashi(chart_5m)
            
            add_swing_high_low(chart_5m)
            
            add_before(chart_5m, 1)
            add_before(chart_5m, 2)
            add_before(chart_5m, 3)
            add_before(chart_5m, 4)
            add_before(chart_5m, 5)
            
            chart = pandas.DataFrame()
            
            # chart['a'] = chart_5m[chart_5m['SwingHigh'] > 0]
            chart = chart_5m[chart_5m['SwingHigh'] > 0]
            print(chart['SwingHigh'].tail(10))
            
            chart = chart_5m[chart_5m['SwingLow'] > 0]
            print(chart['SwingLow'].tail(10))
            
        else:
            print(f"{file_name} is not exsisted.")
            
    
        


#       短期、      中期、      長期　       長期2       長期3
# 1M,   5M,         20M,        60M        100M=1H40M  200M=3H20M
# 5M,   25M,        100M=1H40M, [300M=5H]  500M=8H20M  1000M
# 15M,  75M=1H15M,  [300M=5H],  900M=15H   1500M=25H
# 1H,   [5H],       20H,        60H=2D12H
# 4H,   20H,        80H=3D8H,   240H=10D
# 8H,   40H=1D16H,  160H=6D16H, 480H=20D
# 1D,   5D,         20D,        60D
# 1W,   20D=1M,     60D=3M,        120D=6M

