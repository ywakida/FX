from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG


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

def EMA(arr: pandas.Series, n: int) -> pandas.Series:
    """
    Returns `n`-period  exponential moving average of array `arr`.
    """
    return pandas.Series(arr).ewm(span=n, adjust=False).mean()

def RSI(arr: pandas.Series, n: int) -> pandas.Series:
    """Relative strength index"""
    # Approximate; good enough
    gain = pandas.Series(arr).diff()
    loss = gain.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    rs = gain.ewm(n).mean() / loss.abs().ewm(n).mean()
    return 100 - 100 / (1 + rs)

class myStrategy1(Strategy):
    """
    値が2連続で上がっていたら、利確と損切の価格を設定して買い注文を入れるストラテジー
    """
    def init(self): # ストラテジーの事前処理
        return # 何もしない
        
    def next(self): # ヒストリカルデータの行ごとに呼び出される（データの2行目から開始）
        if not self.position: # ポジションを持っていない場合
            if len(self.data) >= 3: # ヒストリカルデータの3行目以降の場合
                if self.data.Close[-1] > self.data.Close[-2]: # 現在の終値が１つ前の終値より上回っている場合
                    if self.data.Close[-2] > self.data.Close[-3]: # １つ前の終値が２つ前の終値より上回っている場合
                          self.buy(
                             tp=self.data.Close[-1] + 0.30, # tp（take profit）利確する価格を設定、現在の価格+0.3
                             sl=self.data.Close[-1] - 0.20 # sl（stop losst）損切りする価格を設定、現在の価格-0.3
                          )

class myStrategy(Strategy):
    """
    ポジションがないなら買い注文をして、時間が10行分経過したら現在の価格でクローズするストラテジー
    """
    def init(self): # ストラテジーの事前処理
        return # 何もしない
        
    def next(self): # ヒストリカルデータの行ごとに呼び出される（データの2行目から開始）
        if not self.position: # ポジションを持っていない場合
            self.orderd_bar = len(self.data)  # 現在の行数を取得
            self.buy() # 買い注文を出す
        else:  # ポジションを持っている場合
            if len(self.data) > self.orderd_bar + 10: # 買い注文から10行分経過した場合
                self.position.close() # 現在の価格でポジションをクローズする
                

class SmaCross(Strategy):
    n1 = 5
    n2 = 20
    n3 = 60

    def init(self):
        self.smaS = self.I(SMA, self.data.Close, self.n1)
        self.smaM = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        if crossover(self.smaS, self.smaM):
            self.buy()
        elif crossover(self.smaM, self.smaS):
            self.position.close()
            
                            
class EmaCross(Strategy):
    n1 = 20
    n2 = 60

    def init(self):
        self.smaM = self.I(EMA, self.data.Close, self.n1)
        self.smaL = self.I(EMA, self.data.Close, self.n2)

    def next(self):
        if crossover(self.smaM, self.smaL):
            self.buy()
        elif crossover(self.smaL, self.smaM):
            self.sell()
            
class RsiCross(Strategy):
    ns = 14 # 短期
    nl = 28 # 長期

    def init(self):
        self.rsiS = self.I(RSI, self.data.Close, self.ns)
        self.rsiL = self.I(RSI, self.data.Close, self.nl)

    def next(self):
        if crossover(self.rsiS, self.rsiL):
            self.buy()
        elif crossover(self.rsiL, self.rsiS):
            self.position.close()
            
            

def analyze():
    currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'NZDJPY', 'CADJPY', 'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'CADUSD']
    currencies = ['USDJPY']
    
    print(datetime.datetime.now())
    # for ohlc in [ohlc_usdjpy, ohlc_eurjpy, ohlc_gbpjpy, ohlc_eurusd, ohlc_gbpusd]:
    # for ohlc in [ohlc_usdjpy, ohlc_eurjpy, ohlc_gbpjpy]:
    for ohlc in [ohlc_usdjpy]:

        print (' ', ohlc.ticker, ':', '15minute', ' - ', ohlc.m15_updated)
        chart = ohlc.h1
        
        bt = Backtest(
            chart.tail(300), # ヒストリカルデータ
            RsiCross, # ストラテジー
            cash=10000, # 所持金
            commission=.002, # 取引手数料
            exclusive_orders=True # True:現在の終値で取引する、False:次の時間の始値で取引する
            )
        output = bt.run()
        print(output)
        # output._equity_curve["Equity"].plot()
        bt.plot()
            
if __name__ == "__main__":
    
    os.system('cls')

    # pandasのprint表示の仕方を設定
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.width', 1000)
    
    analyze()

 
            
