
import streamlit as st
from datetime import date
from indicadores.tecnicos import get_stock_data
from indicadores.estrategias import (
    apply_crossover_strategy,
    bollinger_breakout_strategy,
    rsi_macd_strategy,
)
from utils.performance import calculate_performance_metrics, apply_stop_loss_take_profit
from utils.relatorios import gerar_relatorio_pdf, gerar_relatorio_docx
import plotly.graph_objects as go

st.set_page_config(page_title="Backtest B3", layout="wide")
st.title("📈 Backtest de Estratégias - B3")

# Seleção de ativo e datas
tickers = st.multiselect("Selecione os ativos", ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA"], default=["PETR4.SA"])
start_date = st.date_input("Data inicial", value=date(2022, 1, 1))
end_date = st.date_input("Data final", value=date.today())

estrategia = st.selectbox("Estratégia", ["Cruzamento de Médias", "Breakout Bollinger", "RSI + MACD"])

col1, col2 = st.columns(2)
with col1:
    sma_fast = st.number_input("SMA Curta", 1, 100, 20)
with col2:
    sma_slow = st.number_input("SMA Longa", 1, 200, 50)

col3, col4 = st.columns(2)
with col3:
    stop_loss = st.slider("Stop Loss (%)", 0.0, 20.0, 5.0) / 100
with col4:
    take_profit = st.slider("Take Profit (%)", 0.0, 50.0, 10.0) / 100

resultados = []

if st.button("🚀 Executar Backtest"):
    for ticker in tickers:
        df = get_stock_data(ticker, str(start_date), str(end_date), sma_periods=[sma_fast, sma_slow])
        if df is None:
            st.warning(f"Não foi possível carregar dados para {ticker}")
            continue

        if estrategia == "Cruzamento de Médias":
            df = apply_crossover_strategy(df, f'SMA_{sma_fast}', f'SMA_{sma_slow}')
        elif estrategia == "Breakout Bollinger":
            df = bollinger_breakout_strategy(df)
        elif estrategia == "RSI + MACD":
            df = rsi_macd_strategy(df)

        df = apply_stop_loss_take_profit(df, stop_loss, take_profit)
        metrics = calculate_performance_metrics(df)
        resultados.append((ticker, df, metrics))

        st.subheader(f"📊 Resultados para {ticker}")
        st.write(metrics)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Preço'))
        if f'SMA_{sma_fast}' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[f'SMA_{sma_fast}'], name=f'SMA {sma_fast}'))
        if f'SMA_{sma_slow}' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[f'SMA_{sma_slow}'], name=f'SMA {sma_slow}'))
        buy = df[df['Signal'] == 1]
        sell = df[df['Signal'] == -1]
        fig.add_trace(go.Scatter(x=buy.index, y=buy['Close'], mode='markers', marker_symbol='triangle-up', marker_color='green', name='Compra'))
        fig.add_trace(go.Scatter(x=sell.index, y=sell['Close'], mode='markers', marker_symbol='triangle-down', marker_color='red', name='Venda'))
        fig.update_layout(title=f"{ticker} - Sinais de Compra/Venda", xaxis_title="Data", yaxis_title="Preço")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📄 Relatórios"):
            parametros = {
                "Ticker": ticker,
                "Estratégia": estrategia,
                "SMA Curta": sma_fast,
                "SMA Longa": sma_slow,
                "Stop Loss": f"{stop_loss*100:.1f}%",
                "Take Profit": f"{take_profit*100:.1f}%",
                "Período": f"{start_date} a {end_date}"
            }
            colpdf, coldocx = st.columns(2)
            with colpdf:
                if st.button(f"📥 PDF - {ticker}"):
                    caminho_pdf = gerar_relatorio_pdf(ticker, df, metrics, fig, parametros)
                    with open(caminho_pdf, "rb") as f:
                        st.download_button("Baixar PDF", f, file_name=f"relatorio_{ticker}.pdf")
            with coldocx:
                if st.button(f"📥 DOCX - {ticker}"):
                    caminho_docx = gerar_relatorio_docx(ticker, df, metrics, fig, parametros)
                    with open(caminho_docx, "rb") as f:
                        st.download_button("Baixar DOCX", f, file_name=f"relatorio_{ticker}.docx")

    if resultados:
        df_ranking = []
        for ticker, _, metrics in resultados:
            df_ranking.append({"Ativo": ticker, **metrics})
        import pandas as pd
        df_ranking = pd.DataFrame(df_ranking).sort_values(by="Retorno Acumulado (%)", ascending=False)
        st.subheader("🏆 Ranking de Ativos")
        st.dataframe(df_ranking.reset_index(drop=True))
