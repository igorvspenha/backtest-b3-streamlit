
import pandas as pd

def apply_crossover_strategy(df: pd.DataFrame, fast_col: str, slow_col: str) -> pd.DataFrame:
    df = df.copy()
    df['Signal'] = 0
    df.loc[(df[fast_col] > df[slow_col]) & (df[fast_col].shift(1) <= df[slow_col].shift(1)), 'Signal'] = 1
    df.loc[(df[fast_col] < df[slow_col]) & (df[fast_col].shift(1) >= df[slow_col].shift(1)), 'Signal'] = -1
    return df

def bollinger_breakout_strategy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Signal'] = 0
    df.loc[df['Close'] > df['Bollinger_Upper'], 'Signal'] = 1
    df.loc[df['Close'] < df['Bollinger_Lower'], 'Signal'] = -1
    df['Signal'] = df['Signal'].replace(0, method='ffill')
    return df

def rsi_macd_strategy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Signal'] = 0
    buy_condition = (df['RSI'] < 30) & (df['MACD'] > df['MACD_signal']) & (df['MACD'].shift(1) <= df['MACD_signal'].shift(1))
    sell_condition = (df['RSI'] > 70) & (df['MACD'] < df['MACD_signal']) & (df['MACD'].shift(1) >= df['MACD_signal'].shift(1))
    df.loc[buy_condition, 'Signal'] = 1
    df.loc[sell_condition, 'Signal'] = -1
    df['Signal'] = df['Signal'].replace(0, method='ffill').fillna(0)
    return df
