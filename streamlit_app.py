import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Título do painel
st.set_page_config(page_title="Painel Bitcoin Pro", layout="wide")
st.title("📊 Painel de Análise Profissional do Bitcoin")
st.markdown("🚀 Métricas gráficas + Ciclos + Estratégias de Bull/Bear Market")

# Intervalo de datas
start = st.sidebar.date_input("Data inicial", value=datetime(2013, 1, 1))
end = st.sidebar.date_input("Data final", value=datetime.today())

# Baixa dados do BTC
btc = yf.download("BTC-USD", start=start, end=end)
btc.dropna(inplace=True)

# RSI Estocástico (simplificado)
def stochastic_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    stoch_rsi = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
    return stoch_rsi

btc['StochRSI'] = stochastic_rsi(btc)

# Fibonacci - projeção
def fibonacci_levels_
