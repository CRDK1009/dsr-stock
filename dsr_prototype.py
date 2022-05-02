import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from stockstats import StockDataFrame
st.title('Stock Guru') 
st.markdown("_~ C R Deepak Kumar_")
st.markdown("_You can now access Stocks in National Stock Exchange(NSE), Bombay Stock Exchange(BSE), NASDAQ and Crypto-Currencies_")
st.markdown("_Example:_")
st.markdown("_Larsen & Toubro in NSE - 'LT.NS'_")
st.markdown("_Larsen & Toubro in BSE - 'LT.BO'_")
st.markdown("_GOOGLE in NASDAQ - 'GOGGL'_")
st.markdown("_DOGECOIN in India - 'DOGE-INR'_")
st.markdown("_DOGECOIN in US - 'DOGE-USD'_")


st.markdown("_A stock's shares has already been loaded for the user to show how the application works_")
a=st.text_input('Company for Analysis','IDEA.NS')
Stocks_data=yf.download(a,period='6mo')
st.markdown("_A snippet of the data collected_")
st.table(Stocks_data['Adj Close'].head())
Stocks_data['sma_20'] = Stocks_data['Adj Close'].rolling(20).mean()
Stocks_data['sma_50'] = Stocks_data['Adj Close'].rolling(50).mean()
candlestick = go.Candlestick(
    x=Stocks_data.index,
    open=Stocks_data['Open'],
    high=Stocks_data['High'],
    low=Stocks_data['Low'],
    close=Stocks_data['Close'])

# Create a candlestick figure   
fig = go.Figure(data=[candlestick])
fig.add_trace(go.Scatter(x=Stocks_data.index, y=Stocks_data['sma_50'],
                    mode='lines',
                    name='sma_50'))
fig.add_trace(go.Scatter(x=Stocks_data.index, y=Stocks_data['sma_20'],
                    mode='lines',
                    name='sma_20'))

fig.update_layout(height=600, width=1000,
                  title_text="Trend Indicator")
st.plotly_chart(fig)

stockstats_df = StockDataFrame.retype(Stocks_data)

fig_rsi = make_subplots(rows=1, cols=2)

fig_rsi.add_trace(
    go.Scatter(x=Stocks_data.index, y=Stocks_data['adj close']),
    row=1, col=1
)

fig_rsi.add_trace(
    go.Scatter(x=Stocks_data.index, y=stockstats_df['rsi_14']),
    row=1, col=2
)

fig_rsi.update_layout(height=500, width=1000,title_text="Stock vs RSI")
st.plotly_chart(fig_rsi)

fig_bol = go.Figure(data=[candlestick])


fig_bol.add_trace(go.Scatter(x=Stocks_data.index, y=stockstats_df['boll'],
                    mode='lines',
                    name='mid'))
fig_bol.add_trace(go.Scatter(x=Stocks_data.index, y=stockstats_df['boll_ub'],
                    mode='lines',
                    name='upper'))
fig_bol.add_trace(go.Scatter(x=Stocks_data.index, y=stockstats_df['boll_lb'],
                    mode='lines',
                    name='lower'))
fig_bol.update_layout(height=500, width=1000,title_text="Stock vs Bollinger Bands")
st.plotly_chart(fig_bol)

st.markdown("_Finally the user can Check the Investment value by checking the Risk/Reward ratio_")
st.markdown("_Stocks' markets are NSE:'^NSEI', BSE:'^BSESN', NASDAQ: '^IXIC'_")
st.markdown("_A list of five stocks' shares has already been loaded for the user to show how the application works_")
st.markdown("_Time Period Notation: 'm'='Minute', 'd'='Days', 'mo'='Month'_")
st.markdown("_Stocks' markets are NSE:'^NSEI', BSE:'^BSESN', NASDAQ: '^IXIC'_")
if st.checkbox('Intraday Trading'):
    Date=st.selectbox('Select the Period of time',['5m','15m','60m','90m','1d','3d','7d'])
    a=st.text_input('1st Company for Comparision','LT.NS')
    b=st.text_input('2nd Company for Comparision', 'BHEL.NS')
    c=st.text_input('3rd Company for Comparision', 'TCS.NS')
    d=st.text_input('4th Company for Comparision','TATASTEEL.NS')
    e=st.text_input('5th Company for Comparision','WIPRO.NS')
    f=st.text_input('Stocks compared to NSE:^NSEI, BSE:^BSESN, NASDAQ: ^IXIC','^NSEI')
    Stocks=[a,b,c,d,e]
    Stocks_data=yf.download(Stocks,period=Date,interval='1m')
    Nifty=yf.download(f,period=Date,interval='1m')
    st.markdown("_A snippet of the data collected_")
    st.table(Stocks_data['Adj Close'].head())
    
    Data_Close_price=Stocks_data['Adj Close'].join(Nifty['Adj Close'])
    Value=Data_Close_price.pct_change()
    Nifty_Value=Nifty['Adj Close'].pct_change()
    Nifty_Value=pd.DataFrame(Nifty_Value)
    Nifty_Value=Nifty_Value.reset_index()
    Nifty_Value.columns=['Datetime','Adj Close']
    #st.markdown("_Value of the market_")
    import plotly.express as px
    fig = px.line(Nifty_Value, x="Datetime", y=Nifty_Value['Adj Close'])
    #st.plotly_chart(fig)
    stock_returns=Value.drop(['Adj Close'],axis=1)
    sp_returns=Value['Adj Close']
    excess_returns=stock_returns.sub(sp_returns,axis=0)
    avg_excess_return=excess_returns.mean()
    #Returns=pd.DataFrame(avg_excess_return)
    #st.markdown("_Returns in the Stocks_")
    #fig_Return = go.Figure(data=[go.Bar(
                #x=Returns.index, y=Returns[0],
                #text=Returns.index,
                #textposition='auto',
            #)])
    #st.plotly_chart(fig_Return)
    sd_excess_return=excess_returns.std()
    #Risk=pd.DataFrame(sd_excess_return)
    #st.markdown("_Risk in the Stocks_")
    #fig_Risk = go.Figure(data=[go.Bar(
                #x=Risk.index, y=Risk[0],
                #text=Risk.index,
                #textposition='auto',
            #)])
    #st.plotly_chart(fig_Risk)
    daily_sharpe_ratio=avg_excess_return.div(sd_excess_return)
    annual_factor=np.sqrt(252)
    annual_sharpe_ratio=daily_sharpe_ratio.mul(annual_factor)
    Sharpe_ratio=pd.DataFrame(annual_sharpe_ratio)
    st.markdown("_Investment Value according to the Risk & Return present in the Stocks_")
    # Use textposition='auto' for direct text
    fig_Sharpe = go.Figure(data=[go.Bar(
                x=Sharpe_ratio.index, y=Sharpe_ratio[0],
                text=Sharpe_ratio.index,
                textposition='auto',
            )])


    st.plotly_chart(fig_Sharpe)
    #Close_Price=Stocks_data['Adj Close'].iloc[-1,:]
    #st.header('Price')
    #st.table(Close_Price)
    
   
if st.checkbox('Swing and Position Trading'):
    Date=st.selectbox('Select the Period of time',['1mo','2mo','3mo','4mo','5mo','6mo','7mo','8mo','9mo','10mo','11mo','12mo'])
    a=st.text_input('1st Company for Comparision','SAIL.NS')
    b=st.text_input('2nd Company for Comparision', 'ONGC.NS')
    c=st.text_input('3rd Company for Comparision', 'BPCL.NS')
    d=st.text_input('4th Company for Comparision','TATAMOTORS.NS')
    e=st.text_input('5th Company for Comparision','TATAPOWER.NS')
    f=st.text_input('Stocks compared to NSE:^NSEI, BSE:^BSESN, NASDAQ: ^IXIC ','^NSEI')
    Stocks=[a,b,c,d,e]
    Stocks_data=yf.download(Stocks,period=Date)
    Nifty=yf.download(f,period=Date)
    st.markdown("_A snippet of the data collected_")
    st.table(Stocks_data['Adj Close'].head())

    Data_Close_price=Stocks_data['Adj Close'].join(Nifty['Adj Close'])
    Value=Data_Close_price.pct_change()
    Nifty_Value=Nifty['Adj Close'].pct_change()
    Nifty_Value=pd.DataFrame(Nifty_Value)
    Nifty_Value=Nifty_Value.reset_index()
    Nifty_Value.columns=['Datetime','Adj Close']
    #st.markdown("_Value of the market_")
    import plotly.express as px
    fig = px.line(Nifty_Value, x="Datetime", y=Nifty_Value['Adj Close'])
    #st.plotly_chart(fig)
    stock_returns=Value.drop(['Adj Close'],axis=1)
    sp_returns=Value['Adj Close']
    excess_returns=stock_returns.sub(sp_returns,axis=0)
    avg_excess_return=excess_returns.mean()
    #Returns=pd.DataFrame(avg_excess_return)
    #st.markdown("_Returns in the Stocks_")
    #fig_Return = go.Figure(data=[go.Bar(
                #x=Returns.index, y=Returns[0],
                #text=Returns.index,
                #textposition='auto',
            #)])
   # st.plotly_chart(fig_Return)
    sd_excess_return=excess_returns.std()
    #Risk=pd.DataFrame(sd_excess_return)
    #st.markdown("_Risk in the Stocks_")
    #fig_Risk = go.Figure(data=[go.Bar(
                #x=Risk.index, y=Risk[0],
                #text=Risk.index,
                #textposition='auto',
            #)])
    #st.plotly_chart(fig_Risk)
    daily_sharpe_ratio=avg_excess_return.div(sd_excess_return)
    annual_factor=np.sqrt(252)
    annual_sharpe_ratio=daily_sharpe_ratio.mul(annual_factor)
    Sharpe_ratio=pd.DataFrame(annual_sharpe_ratio)
    st.markdown("_Investment Value according to the Risk & Return present in the Stocks_")
    # Use textposition='auto' for direct text
    fig_Sharpe = go.Figure(data=[go.Bar(
                x=Sharpe_ratio.index, y=Sharpe_ratio[0],
                text=Sharpe_ratio.index,
                textposition='auto',
            )])


    st.plotly_chart(fig_Sharpe)
    #Close_Price=Stocks_data['Adj Close'].iloc[-1,:]
    #st.header('Price')
    #st.table(Close_Price)
    
    

