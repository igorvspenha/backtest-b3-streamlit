
import numpy as np
import pandas as pd

def calculate_performance_metrics(df: pd.DataFrame) -> dict:
    df = df.copy()
    df['Position'] = df['Signal'].replace(0, method='ffill').fillna(0)
    df['Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Position'].shift(1) * df['Return']

    cumulative_return = (1 + df['Strategy_Return']).cumprod().iloc[-1] - 1
    cumulative = (1 + df['Strategy_Return']).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()
    sharpe_ratio = np.mean(df['Strategy_Return']) / np.std(df['Strategy_Return']) * np.sqrt(252)

    return {
        'Retorno Acumulado (%)': round(cumulative_return * 100, 2),
        'Drawdown Máximo (%)': round(max_drawdown * 100, 2),
        'Índice de Sharpe': round(sharpe_ratio, 2)
    }

def apply_stop_loss_take_profit(df: pd.DataFrame, stop_loss_pct=0.05, take_profit_pct=0.10) -> pd.DataFrame:
    df = df.copy()
    df['Position'] = 0
    position = 0
    entry_price = 0.0

    for i in range(1, len(df)):
        if df['Signal'].iloc[i] == 1 and position == 0:
            position = 1
            entry_price = df['Close'].iloc[i]
            df.at[df.index[i], 'Position'] = 1
        elif position == 1:
            price = df['Close'].iloc[i]
            if price <= entry_price * (1 - stop_loss_pct) or price >= entry_price * (1 + take_profit_pct):
                position = 0
            df.at[df.index[i], 'Position'] = position
        else:
            df.at[df.index[i], 'Position'] = 0

    df['Position'] = df['Position'].shift(1).fillna(0)
    df['Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Position'] * df['Return']
    return df
