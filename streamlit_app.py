import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import datetime
import numpy as np

# Função para calcular RSI Clássico
def compute_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Função para calcular RSI Estocástico
def compute_stoch_rsi(data, window=14):
    rsi = compute_rsi(data, window)
    stoch_rsi = (rsi - rsi.rolling(window).min()) / (rsi.rolling(window).max() - rsi.rolling(window).min())
    return stoch_rsi * 100

# Função para identificar halvings do Bitcoin
def get_halving_dates():
    return [
        datetime.datetime(2012, 11, 28),
        datetime.datetime(2016, 7, 9),
        datetime.datetime(2020, 5, 11),
        datetime.datetime(2024, 4, 19)
    ]

# Sidebar para parâmetros
st.sidebar.title("Painel Bitcoin Pro")
start_date = st.sidebar.date_input("Data inicial", datetime.date(2018, 1, 1))
end_date = st.sidebar.date_input("Data final", datetime.date.today())

ticker = st.sidebar.selectbox("Ativo", ["BTC-USD", "ETH-USD"])  # Pode expandir

data = yf.download(ticker, start=start_date, end=end_date)

# Calcular RSI e RSI Estocástico
data['RSI'] = compute_rsi(data)
data['StochRSI'] = compute_stoch_rsi(data)

st.title("📊 Painel Profissional de Análise do Bitcoin")

# Gráfico de Preço + RSI
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Preço BTC', line=dict(color='orange')))

# Marcar Halvings
for halving in get_halving_dates():
    if data.index[0] < halving < data.index[-1]:
        fig.add_vline(
            x=halving.strftime('%Y-%m-%d'),
            line=dict(color="blue", dash="dot"),
            annotation_text="Halving",
            annotation_position="top left"
        )

fig.update_layout(title="Gráfico BTC + Halvings", xaxis_title="Data", yaxis_title="Preço (USD)")
st.plotly_chart(fig, use_container_width=True)

# RSI Gráfico
st.subheader("📉 RSI Clássico e RSI Estocástico")
rsi_fig = go.Figure()
rsi_fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI 14', line=dict(color='green')))
rsi_fig.add_trace(go.Scatter(x=data.index, y=data['StochRSI'], name='Stoch RSI', line=dict(color='purple')))
rsi_fig.update_layout(title="RSI e RSI Estocástico", xaxis_title="Data", yaxis_title="Valor RSI")
st.plotly_chart(rsi_fig, use_container_width=True)

st.markdown("---")
st.info("Próximas funções em desenvolvimento: Upload de dados on-chain e geração de relatório em PDF")
