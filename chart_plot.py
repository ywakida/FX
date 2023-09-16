import pandas
import plotly.graph_objects as go
import plotly.offline
import plotly.io
from plotly.subplots import make_subplots

def add_graphsetting(figure):
    """グラフの全体設定
    """
    # 背景やグラフの色の設定
    figure.update_layout(plot_bgcolor="black", paper_bgcolor="grey") # グラフの背景と全体の背景の設定
    figure.update_xaxes(linecolor='black', gridcolor='gray',mirror=True)
    figure.update_yaxes(linecolor='black', gridcolor='gray',mirror=True)
    
    # グラフのサイズ調整
    figure.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    
    # 凡例
    figure.update_layout(showlegend=True) # 表示設定
    figure.update_layout(legend=dict(xanchor='left', yanchor='top')) # 縦揃え、横揃え
    figure.update_layout(legend=dict(bgcolor='gray', bordercolor='white', borderwidth=1)) # 背景色、枠の色、枠の太さ
    figure.update_layout(legend=dict(x=1.002, y=0.98))

    # フォントの設定
    figure.update_layout(font=dict(size=10, color='white'))
    
    return figure

def remove_gap_datetime(figure, chart):
    """空白(GAP)の時刻を除去する
    """
    # print((chart.index[1]-chart.index[0]).seconds)
    minutes = (chart.index[1]-chart.index[0]).seconds / 60
    days = (chart.index[1]-chart.index[0]).days
    
    if days==1:
        d_all = pandas.date_range(start=chart.index[0],end=chart.index[-1], freq='B') # 月から金のデータ期間の完全な時系列を取得する
    else:
        d_all = pandas.date_range(start=chart.index[0],end=chart.index[-1], freq=f'{minutes}T') # データ期間の完全な時系列を取得する
        # for d in d_all:
        #     print(d)
        
    d_obs = [d.strftime("%Y-%m-%d %H:%M:%S") for d in chart.index] #データの時系列を取得する
    # for d in d_obs:
    #     print(d)
    
    d_breaks = [d for d in d_all.strftime("%Y-%m-%d %H:%M:%S").tolist() if not d in d_obs] # データに含まれていない時刻を抽出
    # for d in d_breaks:
    #     print(d)
    if min==0:
        figure.update_xaxes(rangebreaks=[dict(values=d_breaks)]) # dvalueはmsec    
    else:
        figure.update_xaxes(rangebreaks=[dict(values=d_breaks, dvalue=1000*60*minutes)]) # dvalueはmsec
    
    return figure

    
def remove_weekend(figure, chart):
    """非表示にする日付(土日)をリストアップ
    """
    d_all = pandas.date_range(start=chart.index[0],end=chart.index[-1]) # 日付リストを取得
    d_obs = [d.strftime("%Y-%m-%d") for d in chart.index] #株価データの日付リストを取得
    d_breaks = [d for d in d_all.strftime("%Y-%m-%d").tolist() if not d in d_obs] # 株価データの日付データに含まれていない日付を抽出
    figure.update_xaxes(rangebreaks=[dict(values=d_breaks)])

    return figure

def add_candlestick_oma(figure, chart, row=1, col=1, keys={"S":5, "M":20, "L":60, "LL":200}):
    """ろうそく足のプロット情報作成
    """
    # y軸名を定義
    figure.update_yaxes(title_text="レート", row=row, col=col)
    
    ###
    # ろうそく足
    figure.add_trace(go.Candlestick(x=chart.index, open=chart['Open'], high=chart['High'], low=chart['Low'], close=chart['Close'], name='OHLC', increasing_line_width=1, increasing_line_color='red', increasing_fillcolor='red', decreasing_line_width=1, decreasing_line_color='lime', decreasing_fillcolor='lime'), row=row, col=col)
    
    # SMA
    key = 'S'
    if keys.get(key) != None:
        value = keys.get(key)
        if f'OMA{value}' in chart.columns:
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'OMA{value}'], name=f'{value} OMA', mode="lines", line=dict(color='yellow', width=1)), row=row, col=col)

    key = 'M'
    if keys.get(key) != None:
        value = keys.get(key)
        if f'OMA{value}' in chart.columns:
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'OMA{value}'], name=f'{value} OMA', mode="lines", line=dict(color='red', width=1)), row=row, col=col)
 
    key = 'L'
    if keys.get(key) != None:
        value = keys.get(key)
        if f'OMA{value}' in chart.columns:
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'OMA{value}'], name=f'{value} OMA', mode="lines", line=dict(color='lime', width=1)), row=row, col=col)
    
    key = 'LL'
    if keys.get(key) != None:
        value = keys.get(key)
        if f'OMA{value}' in chart.columns:
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'OMA{value}'], name=f'{value} OMA', mode="lines", line=dict(color='cyan', width=1)), row=row, col=col)
  
    # スケーリング機能
    if row==1:
        figure.update_layout(xaxis1_rangeslider=dict(visible=False))
    
    if row==2:
        figure.update_layout(xaxis2_rangeslider=dict(visible=False))    
    
    return figure


    
def add_candlestick(figure, chart, row=1, col=1, keys={"S":5, "M":20, "L":60, "LL":200}, show_swing=True, show_bollinger=True, show_order=False):
    """ろうそく足のプロット情報作成
    """
    # y軸名を定義
    figure.update_yaxes(title_text="レート", row=row, col=col)
    
    ###
    # ろうそく足
    figure.add_trace(go.Candlestick(x=chart.index, open=chart['Open'], high=chart['High'], low=chart['Low'], close=chart['Close'], name='OHLC', increasing_line_width=1, increasing_line_color='red', increasing_fillcolor='red', decreasing_line_width=1, decreasing_line_color='lime', decreasing_fillcolor='lime'), row=row, col=col)
    
    # SMA
    key = 'S'
    if keys.get(key) != None:
        value = keys.get(key)
        if f'EMA{value}' in chart.columns:
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'EMA{value}'], name=f'{value} EMA', mode="lines", line=dict(color='yellow', width=1)), row=row, col=col)

    key = 'M'
    if keys.get(key) != None:
        value = keys.get(key)
        if f'EMA{value}' in chart.columns:
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'EMA{value}'], name=f'{value} EMA', mode="lines", line=dict(color='red', width=1)), row=row, col=col)
 
        # ボリンジャーバンド
        if show_bollinger:
            if f'BB{value}P2' in chart.columns:
                figure.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{value}P2'], name=f'{value} BB + 2', mode="lines", line=dict(dash='dot', color='pink', width=1)), row=row, col=col)
            if f'BB{value}P1' in chart.columns:
                figure.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{value}P1'], name=f'{value} BB + 1', mode="lines", line=dict(dash='dot', color='pink', width=1)), row=row, col=col)
            if f'BB{value}M1' in chart.columns:
                figure.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{value}M1'], name=f'{value} BB - 1', mode="lines", line=dict(dash='dot', color='pink', width=1)), row=row, col=col)
            if f'BB{value}M2' in chart.columns:
                figure.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{value}M2'], name=f'{value} BB - 2', mode="lines", line=dict(dash='dot', color='pink', width=1)), row=row, col=col)
           
    key = 'L'
    if keys.get(key) != None:
        value = keys.get(key)
        if f'EMA{value}' in chart.columns:
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'EMA{value}'], name=f'{value} EMA', mode="lines", line=dict(color='lime', width=1)), row=row, col=col)
    
    key = 'LL'
    if keys.get(key) != None:
        value = keys.get(key)
        if f'SMA{value}' in chart.columns:
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'SMA{value}'], name=f'{value} SMA', mode="lines", line=dict(color='cyan', width=1)), row=row, col=col)
  
    # スイングハイ・スイングロー
    if show_swing:
        if f'SwingHigh' in chart.columns:
            figure.add_trace(go.Scatter(x=chart[chart["SwingHigh"]>0].index, y=chart[chart["SwingHigh"]>0]["High"]*1.0002, name="高値", mode="markers", marker_symbol="triangle-down", marker_size=5, marker_color="white"), row=row, col=col)
        if f'SwingLow' in chart.columns:
            figure.add_trace(go.Scatter(x=chart[chart["SwingLow"]>0].index, y=chart[chart["SwingLow"]>0]["Low"]*0.9998, name="低値", mode="markers", marker_symbol="triangle-up", marker_size=5, marker_color="white"), row=row, col=col)

    if show_order:
        if 'Buy' in chart.columns:
            figure.add_trace(go.Scatter(x=chart[chart["Buy"]].index, y=chart[chart["Buy"]]["High"]*1.0002, name="買い", mode="markers", marker_symbol="arrow-right", marker_size=5, marker_color="white"), row=row, col=col)
        if 'Sell' in chart.columns:
            figure.add_trace(go.Scatter(x=chart[chart["Sell"]].index, y=chart[chart["Sell"]]["Low"]*0.9998, name="売り", mode="markers", marker_symbol="arrow-left", marker_size=5, marker_color="white"), row=row, col=col)
            
             
    # スケーリング機能
    if row==1:
        figure.update_layout(xaxis1_rangeslider=dict(visible=False))
    if row==2:
        figure.update_layout(xaxis2_rangeslider=dict(visible=False))    
    if row==3:
        figure.update_layout(xaxis3_rangeslider=dict(visible=False))
        
    return figure


def add_rci(figure, chart, row=1, col=1):
    """平均足のプロット情報作成
    """   
    # y軸名を定義
    figure.update_yaxes(title_text="rci", row=row, col=col)
    
    if f'Rci' in chart.columns:
        figure.add_trace(go.Scatter(x=chart.index, y=chart[f'Rci'], name=f'RCI', mode="lines", line=dict(color='yellow', width=2)), row=row, col=col)

    return figure
    
    
def add_heikinashi_candlestick(figure, chart, row=1, col=1):
    """平均足のプロット情報作成
    """   
    # y軸名を定義
    figure.update_yaxes(title_text="平均足", row=row, col=col)
    
    # ろうそく足
    figure.add_trace(go.Candlestick(x=chart.index, open=chart['HA_Open'], high=chart['HA_High'], low=chart['HA_Low'], close=chart['HA_Close'], name='Heikinashi', increasing_line_width=1, increasing_line_color='red', increasing_fillcolor='red', decreasing_line_width=1, decreasing_line_color='green', decreasing_fillcolor='green'), row=row, col=col )
    
    # スケーリング機能
    if row==1:
        figure.update_layout(xaxis1_rangeslider=dict(visible=False))
    if row==2:
        figure.update_layout(xaxis2_rangeslider=dict(visible=False))    
    
    return figure


def add_heikinashi_bar(figure, chart, row=1, col=1, keys={"S":5, "M":20, "L":60, "LL":200}):
    """平均足のプロット情報作成
    """
    # y軸名を定義
    figure.update_yaxes(title_text="平均足(Bar)", row=row, col=col)
    
    figure.add_trace(go.Bar(x=chart[chart['HA_3V']>0].index, y=chart[chart['HA_3V']>0]['HA_3V'], name='平均足陽線', marker=dict(color='red')), row=row, col=col)
    figure.add_trace(go.Bar(x=chart[chart['HA_3V']<0].index, y=chart[chart['HA_3V']<0]['HA_3V']*-1, name='平均足陰線', marker=dict(color='lime')), row=row, col=col)
      
    return figure

def add_deviationrate(figure, chart, row=1, col=1, keys={"S":5, "M":20, "L":60, "LL":200}):
    """乖離率の追加
    """
    colors={"S":"yellow", "M":"red", "L":"lime", "LL":"cyan"}
    
    figure.update_yaxes(title_text="乖離率", row=2, col=1)    
    
    for key, value in keys.items():
        thiscolor = colors.get(key)
        if f'EMADR{value}' in chart.columns:
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'EMADR{value}'], name=f'{value} EMADR', mode="lines", line=dict(color=thiscolor, width=2)), row=row, col=col)
        elif f'SMADR{value}' in chart.columns:
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'SMADR{value}'], name=f'{value} SMADR', mode="lines", line=dict(color=thiscolor, width=2)), row=row, col=col)
        else:
            pass
      
    return figure

def add_sigma(figure, chart, row=1, col=1, keys={"S":5, "M":20, "L":60, "LL":200}):
    """シグマの追加
    """
    colors={"S":"yellow", "M":"red", "L":"lime", "LL":"cyan"}
    
    figure.update_yaxes(title_text="シグマ", row=2, col=1)
    
    for key, value in keys.items():
        thiscolor = colors.get(key)
        
        if f'SIGMA{value}' in chart.columns:
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'SIGMA{value}'], name=f'{value} SIGMA', mode="lines", line=dict(color=thiscolor, width=2)), row=row, col=col)
      
    return figure

def add_slope(figure, chart, row=1, col=1, keys={"S":5, "M":20, "L":60, "LL":200}):
    """乖離率の追加
    """
    colors={"S":"yellow", "M":"red", "L":"lime", "LL":"cyan"}
    
    figure.update_yaxes(title_text="傾き", row=2, col=1)
    
    for key, value in keys.items():
        thiscolor = colors.get(key)
        
        if f'Slope{value}' in chart.columns:     
            figure.add_trace(go.Scatter(x=chart.index, y=chart[f'Slope{value}'], name=f'{value} Slope', mode="lines", line=dict(color=thiscolor, width=2)), row=row, col=col)

    return figure

def plot_basicchart_oma(filename, currency, chart, auto_open=False, keys={"S":5, "M":20, "L":60, "LL":200}):
    """ろうそく足のプロット
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.5, 0.5], x_title="Date")

    # グラフの設定
    fig = add_graphsetting(fig)

    fig = add_candlestick(fig, chart, 1, 1, keys, show_swing=False, show_bollinger=False)
    
    fig = add_candlestick_oma(fig, chart, 2, 1, keys)

    fig = remove_gap_datetime(fig, chart)

    # プロット
    plotly.offline.plot(fig, filename=filename, auto_open=auto_open)
    

def plot_basicchart(filename, currency, chart, auto_open=False, keys={"S":5, "M":20, "L":60, "LL":200}):
    """ろうそく足のプロット
    """
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[1.0], x_title="Date")

    # グラフの設定
    fig = add_graphsetting(fig)

    fig = add_candlestick(fig, chart, 1, 1, keys)

    fig = remove_gap_datetime(fig, chart)

    # プロット
    plotly.offline.plot(fig, filename=filename, auto_open=auto_open)


def plot_with_dr(filename, currency, chart, auto_open=False, keys={"S":5, "M":20, "L":60, "LL":200}):
    """乖離率とのプロット
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.7, 0.3], x_title="Date")
    
    # グラフの設定
    fig = add_graphsetting(fig)
    
    fig = add_candlestick(fig, chart, 1, 1, keys)
    fig = add_deviationrate(fig, chart, 2, 1, keys)
    
    fig = remove_gap_datetime(fig, chart)
    
    # プロット
    plotly.offline.plot(fig, filename=filename, auto_open=auto_open)

def plot_with_sigma(filename, currency, chart, auto_open=False, keys={"S":5, "M":20, "L":60, "LL":200}):
    """シグマとのプロット
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.7, 0.3], x_title="Date")
    
    # グラフの設定
    fig = add_graphsetting(fig)
    
    fig = add_candlestick(fig, chart, 1, 1, keys)
    fig = add_sigma(fig, chart, 2, 1, keys)
    
    fig = remove_gap_datetime(fig, chart)
    
    # プロット
    plotly.offline.plot(fig, filename=filename, auto_open=auto_open)

def plot_with_slope(filename, currency, chart, auto_open=False, keys={"S":5, "M":20, "L":60, "LL":200}):
    """スロープとのプロット
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.7, 0.3], x_title="Date")
    
    # グラフの設定
    fig = add_graphsetting(fig)
    
    fig = add_candlestick(fig, chart, 1, 1, keys)
    fig = add_slope(fig, chart, 2, 1, keys)

    fig = remove_gap_datetime(fig, chart)
    
    # プロット
    plotly.offline.plot(fig, filename=filename, auto_open=auto_open)


def plot_with_rci(filename, currency, chart, auto_open=False, keys={"S":5, "M":20, "L":60, "LL":200}):
    """RCIとのプロット
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.7, 0.3], x_title="Date")
    
    # グラフの設定
    fig = add_graphsetting(fig)
    
    fig = add_candlestick(fig, chart, 1, 1, keys)
    fig = add_rci(fig, chart, 2, 1)
    
    fig = remove_gap_datetime(fig, chart)
    
    # プロット
    plotly.offline.plot(fig, filename=filename, auto_open=auto_open)
    
def plot_with_heikinashi_candlestick(filename, currency, chart, auto_open=False, keys={"S":5, "M":20, "L":60, "LL":200}):
    """平均足チャートとのプロット
    """
    # fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[1.0], x_title="Date")
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.8, 0.2], x_title="Date")
    
    # グラフの設定
    fig = add_graphsetting(fig)
    
    fig = add_candlestick(fig, chart, 1, 1)
    fig = add_heikinashi_candlestick(fig, chart, 1, 1)
    fig = add_rci(fig, chart, row=2, col=1)
    
    fig = remove_gap_datetime(fig, chart)
    
    # プロット
    plotly.offline.plot(fig, filename=filename, auto_open=auto_open)

def plot_with_heikinashi_bar(filename, currency, chart, auto_open=False, keys={"S":5, "M":20, "L":60, "LL":200}):
    """平均足チャートとのプロット

    Args:
        filename (_type_): _description_
        currency (_type_): _description_
        chart (_type_): _description_
        auto_open (bool, optional): _description_. Defaults to False.
        keys (dict, optional): _description_. Defaults to {"S":5, "M":20, "L":60, "LL":200}.
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.9, 0.1], x_title="Date")
    
    # グラフの設定
    fig = add_graphsetting(fig)
    
    fig = add_candlestick(fig, chart, 1, 1)
    fig = add_heikinashi_bar(fig, chart, 2, 1)
    
    fig = remove_gap_datetime(fig, chart)
    
    # プロット
    plotly.offline.plot(fig, filename=filename, auto_open=auto_open)

def plot_for_simulation(filename, currency, chart, auto_open=False, keys={"S":5, "M":20, "L":60, "LL":200}):
    """シグマとのプロット
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.7, 0.3], x_title="Date")
    
    # グラフの設定
    fig = add_graphsetting(fig)
    
    fig = add_candlestick(fig, chart, 1, 1, keys, False, False, True)
    fig = add_rci(fig, chart, 2, 1)
    
    fig = remove_gap_datetime(fig, chart)
    
    return fig


def plotly_show(filename, currency, chart, auto_open=False):
    
    fig = go.Figure()
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.5, 0.5, 0.1, 0.1], x_title="Date")
    
    fig.update_layout(title={'text': f'{currency}', 'y':0.99, 'x':0.5})
    # fig.update_layout(title={'text': f'{ticker}', 'y':0.9, 'x':0.5})
    fig.update_layout(margin=dict(t=20, b=0, l=0, r=0))
    
    fig.update_layout(plot_bgcolor="black")
    fig.update_xaxes(linecolor='black', gridcolor='gray',mirror=True)
    fig.update_yaxes(linecolor='black', gridcolor='gray',mirror=True)


    # y軸名を定義
    fig.update_yaxes(title_text="レート", row=1, col=1)
    fig.update_yaxes(title_text="レート(平均足)", row=2, col=1)
    fig.update_yaxes(title_text="test", row=3, col=1)
    # fig.update_yaxes(title_text="シグマ", row=4, col=1)
    # fig.update_yaxes(title_text="パーフェクトオーダー", row=5, col=1)
    # fig.update_yaxes(title_text="下落率(%", row=6, col=1)
    
    ###
    # ろうそく足
    fig.add_trace(go.Candlestick(x=chart.index, open=chart['Open'], high=chart['High'], low=chart['Low'], close=chart['Close'], name='OHLC', increasing_line_width=1, increasing_line_color='red', increasing_fillcolor='red', decreasing_line_width=1, decreasing_line_color='lime', decreasing_fillcolor='lime'), row=1, col=1 )
    
    # SMA
    param = 5
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'SMA{param}'], name=f'{param} SMA', mode="lines", line=dict(color='yellow', width=1)), row=1, col=1)
    param = 20
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'SMA{param}'], name=f'{param} SMA', mode="lines", line=dict(color='orange', width=1)), row=1, col=1)
    param = 60
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'SMA{param}'], name=f'{param} SMA', mode="lines", line=dict(color='lime', width=1)), row=1, col=1)
    
    # ボリンジャーバンド
    param = 5
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}P2'], name=f'{param} BB + 2', mode="lines", line=dict(dash='dot', color='blue', width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}P1'], name=f'{param} BB + 1', mode="lines", line=dict(dash='dot', color='cyan', width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}M1'], name=f'{param} BB - 1', mode="lines", line=dict(dash='dot', color='cyan', width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}M2'], name=f'{param} BB - 2', mode="lines", line=dict(dash='dot', color='blue', width=1)), row=1, col=1)
    # param = 20
    # fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}P2'], name=f'{param} BB + 2', mode="lines", line=dict(dash='dot', color='pink', width=1)), row=1, col=1)
    # fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}P1'], name=f'{param} BB + 1', mode="lines", line=dict(dash='dot', color='pink', width=1)), row=1, col=1)
    # fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}M1'], name=f'{param} BB - 1', mode="lines", line=dict(dash='dot', color='pink', width=1)), row=1, col=1)
    # fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}M2'], name=f'{param} BB - 2', mode="lines", line=dict(dash='dot', color='pink', width=1)), row=1, col=1)
    
    
    # スイングハイ・スイングロー
    fig.add_trace(go.Scatter(x=chart[chart["SwingHigh"]>0].index, y=chart[chart["SwingHigh"]>0]["High"], name="高値", mode="markers", marker_symbol="triangle-down", marker_size=5, marker_color="black"), row=1, col=1)
    fig.add_trace(go.Scatter(x=chart[chart["SwingLow"]>0].index, y=chart[chart["SwingLow"]>0]["Low"], name="低値", mode="markers", marker_symbol="triangle-up", marker_size=5, marker_color="black"), row=1, col=1)
    # 売られすぎ
    # fig.add_trace(go.Scatter(x=chart[chart["Boraku"]>=1].index, y=chart[chart["Boraku"]>=1]["Low"]*0.99, name="売られすぎ1.0", mode="markers", marker_symbol="triangle-down", marker_size=5, marker_color="black"), row=1, col=1)
    # fig.add_trace(go.Scatter(x=chart[chart["Boraku"]>=2].index, y=chart[chart["Boraku"]>=2]["Low"]*0.98, name="売られすぎ1.5", mode="markers", marker_symbol="triangle-down", marker_size=5, marker_color="black"), row=1, col=1)
    # fig.add_trace(go.Scatter(x=chart[chart["Boraku"]>=3].index, y=chart[chart["Boraku"]>=3]["Low"]*0.97, name="売られすぎ2.0", mode="markers", marker_symbol="triangle-down", marker_size=5, marker_color="black"), row=1, col=1)
    # fig.add_trace(go.Scatter(x=chart[chart["Boraku"]>=4].index, y=chart[chart["Boraku"]>=4]["Low"]*0.96, name="売られすぎ2.5", mode="markers", marker_symbol="triangle-down", marker_size=5, marker_color="black"), row=1, col=1)
    # fig.add_trace(go.Scatter(x=chart[chart["Boraku"]>=5].index, y=chart[chart["Boraku"]>=5]["Low"]*0.95, name="売られすぎ3.0", mode="markers", marker_symbol="triangle-down", marker_size=5, marker_color="black"), row=1, col=1)
    # fig.add_trace(go.Scatter(x=chart[(chart["SIGMA5"]<-1.0)&(chart["Low"]>chart["SMA75"])&(chart["Perfect"]>=3)&(chart["Parallel"]>-1.0)].index, y=chart[(chart["SIGMA5"]<-1.0)&(chart["Low"]>chart["SMA75"])&(chart["Perfect"]>=3)&(chart["Parallel"]>-1.0)]["Close"]*0.98, name="売られすぎ", mode="markers", marker_symbol="triangle-up", marker_size=5, marker_color="black"), row=1, col=1)

    ###
    # 平均足チャート
    fig.add_trace(go.Candlestick(x=chart.index, open=chart['HA_Open'], high=chart['HA_High'], low=chart['HA_Low'], close=chart['HA_Close'], name='OHLC', increasing_line_width=1, increasing_line_color='red', increasing_fillcolor='red', decreasing_line_width=1, decreasing_line_color='lime', decreasing_fillcolor='lime'), row=2, col=1 )
    
    # 指数移動平均
    param = 5
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'EMA{param}'], name=f'{param} EMA', mode="lines", line=dict(color='yellow', width=1)), row=2, col=1)
    param = 20
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'EMA{param}'], name=f'{param} EMA', mode="lines", line=dict(color='orange', width=1)), row=2, col=1)
    param = 60
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'EMA{param}'], name=f'{param} EMA', mode="lines", line=dict(color='lime', width=1)), row=2, col=1)
    
    # ボリンジャーバンド
    param = 5
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}P2'], name=f'{param} BB + 2', mode="lines", line=dict(dash='dot', color='blue', width=1)), row=2, col=1)
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}P1'], name=f'{param} BB + 1', mode="lines", line=dict(dash='dot', color='cyan', width=1)), row=2, col=1)
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}M1'], name=f'{param} BB - 1', mode="lines", line=dict(dash='dot', color='cyan', width=1)), row=2, col=1)
    fig.add_trace(go.Scatter(x=chart.index, y=chart[f'BB{param}M2'], name=f'{param} BB - 2', mode="lines", line=dict(dash='dot', color='blue', width=1)), row=2, col=1)
    
    # 反転
    fig.add_trace(go.Scatter(x=chart[chart["HA_Reversal_Plus"]==True].index, y=chart[chart["HA_Reversal_Plus"]==True]["HA_High"], name="転換", mode="markers", marker_symbol="star", marker_size=5, marker_color="black"), row=2, col=1)
    fig.add_trace(go.Scatter(x=chart[chart["HA_Reversal_Minus"]==True].index, y=chart[chart["HA_Reversal_Minus"]==True]["HA_Low"], name="転換", mode="markers", marker_symbol="star", marker_size=5, marker_color="black"), row=2, col=1)
    
    ###
    # 15分足の平均足の色
    fig.add_trace(go.Bar(x=chart[chart['HA_3V_15M']>0].index, y=chart[chart['HA_3V_15M']>0]['HA_3V_15M'], name='15分平均足陽線', marker=dict(color='red')), row=3, col=1)
    fig.add_trace(go.Bar(x=chart[chart['HA_3V_15M']<0].index, y=chart[chart['HA_3V_15M']<0]['HA_3V_15M'], name='15分平均足陰線', marker=dict(color='lime')), row=3, col=1)

    ###
    # 1時間足の平均足の色
    fig.add_trace(go.Bar(x=chart[chart['HA_3V_1H']>0].index, y=chart[chart['HA_3V_1H']>0]['HA_3V_1H'], name='1時間平均足', marker=dict(color='red')), row=4, col=1)
    fig.add_trace(go.Bar(x=chart[chart['HA_3V_1H']<0].index, y=chart[chart['HA_3V_1H']<0]['HA_3V_1H'], name='1時間平均足', marker=dict(color='lime')), row=4, col=1)
        
    ###
    # ライン
    # param = 60
    # fig.add_trace(go.Scatter(x=chart.index, y=chart[f'SlopeSlope{param}'], name=f'{param} SlopeSlope', mode="lines", line=dict(color='red', width=2)), row=3, col=1)
    # fig.add_trace(go.Scatter(x=chart.index, y=chart[f'Slope{param}'], name=f'{param} Slope', mode="lines", line=dict(color='blue', width=2)), row=3, col=1)
    # fig.add_trace(go.Scatter(x=chart.index, y=chart["DR20"], name="20days DR", mode="lines", line=dict(color='blue', width=2)), row=3, col=1)
    
    # # Sigma
    # fig.add_trace(go.Scatter(x=chart.index, y=chart["SIGMA5"], name="5days SIGMA", mode="lines", line=dict(color='red', width=2)), row=4, col=1)
    # fig.add_trace(go.Scatter(x=chart.index, y=chart["SIGMA20"], name="20days SIGMA", mode="lines", line=dict(color='blue', width=2)), row=4, col=1)
    
    # # Perfect Order
    # fig.add_trace(go.Bar(x=chart.index, y=chart['PerfectOrder'], name='Perfect Order', marker=dict(color='red')), row=5, col=1)
    
    # # Drop
    # fig.add_trace(go.Scatter(x=chart.index, y=chart["Drop5"], name="5days Drop Rate", mode="lines", line=dict(color='red', width=2)), row=6, col=1)
        
    # 非表示にする日付(土日)をリストアップ
    d_all = pandas.date_range(start=chart.index[0],end=chart.index[-1]) # 日付リストを取得
    d_obs = [d.strftime("%Y-%m-%d") for d in chart.index] #株価データの日付リストを取得
    d_breaks = [d for d in d_all.strftime("%Y-%m-%d").tolist() if not d in d_obs] # 株価データの日付データに含まれていない日付を抽出
    fig.update_xaxes(rangebreaks=[dict(values=d_breaks)])
    
    # スケーリング機能
    # fig.update(layout_xaxis_rangeslider=dict(visible=False))
    fig.update_layout(xaxis1_rangeslider=dict(visible=False))
    fig.update_layout(xaxis2_rangeslider=dict(visible=False))
    
    # プロット
    plotly.offline.plot(fig, filename=filename, auto_open=auto_open)
    # plotly.io.write_image(fig, f'{folder_path}/{ticker}.png')
    
    return fig



def plot_test():
    
    import indicator
    print('plot_test')
    
    currencies = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'EURUSD', 'GBPUSD', 'AUDUSD']
    # currencies = ['USDJPY']
    intervals = ['5m', '15m', '1h']
    # intervals = ['1h']
    
    for currency in currencies:
        for interval in intervals:
            file_name = f'ohlc/{currency}_{interval}.csv'
                
            print(f'{file_name}')
            ohlc =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
            
            # タイムゾーンをUTCから変更
            ohlc.index = ohlc.index.tz_convert('Asia/Tokyo')
            ohlc = indicator.add_sigma(ohlc, [20])
            ohlc = indicator.add_ema(ohlc, [5, 20, 60])
            ohlc = indicator.add_sma(ohlc, [200])
            ohlc = indicator.add_ema(ohlc, [4, 12]) # 1分足の中期、長期
            ohlc = indicator.add_ema(ohlc, [15, 60, 180]) # 15分足の短期、中期、長期
            ohlc = indicator.add_swing_high_low(ohlc)
            ohlc = indicator.add_ema_slope(ohlc, [5, 20, 60, 200])
            ohlc = indicator.add_bb(ohlc)
            ohlc = indicator.add_rci(ohlc)
            ohlc = indicator.add_ema_dr(ohlc)
            ohlc = indicator.add_oma(ohlc, [5, 20, 60, 200])
            
            # plot_basicchart_oma(f'html/{currency}_{interval}_oma.html', currency, ohlc.tail(1000), False)
            plot_basicchart(f'html/{currency}_{interval}_basic.html', currency, ohlc.tail(4000), False)
            plot_with_dr(f'html/{currency}_{interval}_with_dr.html', currency, ohlc.tail(4000), False)
            plot_with_rci(f'html/{currency}_{interval}_with_rci.html', currency, ohlc.tail(4000), False)
            plot_with_slope(f'html/{currency}_{interval}_with_slope.html', currency, ohlc.tail(4000), False)
            
            # print(ohlc['Close'].tail(30))
            if interval=='1h':
                # 4時間チャート作成
                ohlc =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
                rule = '4h'
                d_ohlc = {'Open':'first', 'High':'max', 'Low':'min', 'Close':'last'}
                ohlc = ohlc.resample(rule).agg(d_ohlc)
                ohlc = ohlc.dropna()
                
                ohlc = indicator.add_sigma(ohlc, [20])
                ohlc = indicator.add_ema(ohlc, [5, 20, 60])
                ohlc = indicator.add_sma(ohlc, [200])
                ohlc = indicator.add_ema(ohlc, [4, 12]) # 1分足の中期、長期
                ohlc = indicator.add_ema(ohlc, [15, 60, 180]) # 15分足の短期、中期、長期
                ohlc = indicator.add_swing_high_low(ohlc)
                ohlc = indicator.add_ema_slope(ohlc, [5, 20, 60, 200])
                ohlc = indicator.add_bb(ohlc)
                ohlc = indicator.add_rci(ohlc)
                ohlc = indicator.add_ema_dr(ohlc)
                plot_basicchart(f'html/{currency}_{rule}_basic.html', currency, ohlc.tail(4000), False)
                plot_with_dr(f'html/{currency}_{rule}_with_dr.html', currency, ohlc.tail(4000), False)
                plot_with_rci(f'html/{currency}_{rule}_with_rci.html', currency, ohlc.tail(4000), False)
                
                # 日足チャート作成
                ohlc =  pandas.read_csv(file_name, index_col=0, parse_dates=True)
                # print(ohlc.tail(24))
                ohlc.index = ohlc.index + pandas.DateOffset(hours=3)
                # print(ohlc.tail(24))
                
                rule = '1d'
                d_ohlc = {'Open':'first', 'High':'max', 'Low':'min', 'Close':'last'}
                ohlc = ohlc.resample(rule).agg(d_ohlc)
                ohlc = ohlc.dropna()
                    
                ohlc = indicator.add_sigma(ohlc, [20])
                ohlc = indicator.add_ema(ohlc, [5, 20, 60])
                ohlc = indicator.add_sma(ohlc, [200])
                ohlc = indicator.add_ema(ohlc, [4, 12]) # 1分足の中期、長期
                ohlc = indicator.add_ema(ohlc, [15, 60, 180]) # 15分足の短期、中期、長期
                ohlc = indicator.add_swing_high_low(ohlc)
                ohlc = indicator.add_ema_slope(ohlc, [5, 20, 60, 200])
                ohlc = indicator.add_bb(ohlc)
                ohlc = indicator.add_rci(ohlc)
                ohlc = indicator.add_ema_dr(ohlc)
                plot_basicchart(f'html/{currency}_{rule}_basic.html', currency, ohlc.tail(4000), False)
                plot_with_dr(f'html/{currency}_{rule}_with_dr.html', currency, ohlc.tail(4000), False)
                plot_with_rci(f'html/{currency}_{rule}_with_rci.html', currency, ohlc.tail(4000), False)

            else:
                print(f"{file_name} is not exsisted.")
            

import os
if __name__ == "__main__":
    
    os.system('cls')

    # pandasのprint表示の仕方を設定
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.width', 1000)
    
    plot_test()

    keys={"S":[5, "green"], "M":[20, "red"], "L":[60, "yellow"], "LL":[200, "lyme"]}
    
    