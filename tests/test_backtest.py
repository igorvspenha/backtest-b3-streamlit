
import pandas as pd
from indicadores.estrategias import apply_crossover_strategy, bollinger_breakout_strategy, rsi_macd_strategy
from utils.performance import calculate_performance_metrics

def criar_df_teste():
    dates = pd.date_range(start='2022-01-01', periods=10)
    data = {
        'Close': [10, 10.5, 11, 10.8, 10.6, 10.7, 10.9, 11.1, 11.3, 11.2],
        'SMA_20': [10]*10,
        'SMA_50': [9.8]*10,
        'Bollinger_Upper': [11.2]*10,
        'Bollinger_Lower': [9.5]*10,
        'RSI': [29, 30, 31, 32, 72, 74, 73, 69, 68, 70],
        'MACD': [0.1, 0.12, 0.15, 0.17, -0.2, -0.25, -0.22, -0.19, -0.18, -0.16],
        'MACD_signal': [0.08, 0.10, 0.13, 0.14, -0.18, -0.20, -0.23, -0.20, -0.19, -0.18]
    }
    return pd.DataFrame(data, index=dates)

def test_crossover_strategy():
    df = criar_df_teste()
    df = apply_crossover_strategy(df, 'SMA_20', 'SMA_50')
    assert 'Signal' in df.columns
    assert df['Signal'].max() == 1 or df['Signal'].min() == -1

def test_bollinger_breakout_strategy():
    df = criar_df_teste()
    df = bollinger_breakout_strategy(df)
    assert 'Signal' in df.columns
    assert isinstance(df['Signal'].iloc[-1], (int, float))

def test_rsi_macd_strategy():
    df = criar_df_teste()
    df = rsi_macd_strategy(df)
    assert 'Signal' in df.columns
    assert df['Signal'].dtype in ['int64', 'float64']

def test_calculate_performance_metrics():
    df = criar_df_teste()
    df['Signal'] = [1]*10
    df['Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Return']
    metrics = calculate_performance_metrics(df)
    assert isinstance(metrics, dict)
    assert 'Retorno Acumulado (%)' in metrics
