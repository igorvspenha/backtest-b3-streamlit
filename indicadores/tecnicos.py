
import yfinance as yf
import pandas as pd

def get_stock_data(ticker: str, start_date: str, end_date: str,
                   sma_periods=[20, 50], ema_periods=[20, 50],
                   rsi_period=14, macd_fast=12, macd_slow=26, macd_signal=9,
                   bollinger_period=20):
    df = yf.download(ticker, start=start_date, end=end_date)
    if df.empty:
        return None

    for period in sma_periods:
        df[f'SMA_{period}'] = df['Close'].rolling(window=period).mean()
    for period in ema_periods:
        df[f'EMA_{period}'] = df['Close'].ewm(span=period, adjust=False).mean()

    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(rsi_period).mean()
    loss = -delta.where(delta < 0, 0).rolling(rsi_period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    ema_fast = df['Close'].ewm(span=macd_fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=macd_slow, adjust=False).mean()
    df['MACD'] = ema_fast - ema_slow
    df['MACD_signal'] = df['MACD'].ewm(span=macd_signal, adjust=False).mean()

    ma = df['Close'].rolling(window=bollinger_period).mean()
    std = df['Close'].rolling(window=bollinger_period).std()
    df['Bollinger_Upper'] = ma + (2 * std)
    df['Bollinger_Lower'] = ma - (2 * std)

    df.dropna(inplace=True)
    return df
