# 📈 Backtest B3 Streamlit

Uma aplicação interativa em Python com Streamlit para realizar **backtests de estratégias no mercado acionário brasileiro**, focada em investidores iniciantes.

## 🎯 Funcionalidades

✅ Estratégias técnicas prontas  
✅ Backtest com stop loss / take profit  
✅ Gráficos interativos com sinais de compra e venda  
✅ Exportação de relatórios em PDF e DOCX  
✅ Comparação entre múltiplos ativos (ranking)  
✅ Simulações com janela móvel (rolling window)  

## 📊 Estratégias Implementadas

### 1. Cruzamento de Médias (SMA ou EMA)
Compra quando a média curta cruza acima da longa.  
Venda quando cruza abaixo.

### 2. Breakout com Bandas de Bollinger
Compra quando o fechamento ultrapassa a banda superior.  
Venda quando cai abaixo da banda inferior.

### 3. RSI + MACD
Compra: RSI < 30 e MACD cruzando para cima.  
Venda: RSI > 70 e MACD cruzando para baixo.

## 📈 Métricas Calculadas

- Retorno acumulado (%)
- Drawdown máximo (%)
- Índice de Sharpe
- Curva de capital
- Distribuição dos retornos

## 📥 Exportações

- Relatórios PDF e DOCX
- Arquivo CSV com sinais e indicadores

## 🧪 Backtest Rolling

Permite aplicar a estratégia em janelas móveis (ex: 90 dias).

## 🛠️ Como executar

```bash
git clone https://github.com/seu-usuario/backtest-b3-streamlit.git
cd backtest-b3-streamlit
pip install -r requirements.txt
streamlit run app.py
```

## 👨‍💻 Autor

Desenvolvido por [Seu Nome], como parte do projeto de pós-graduação em Análise de Dados para o Mercado Financeiro.
