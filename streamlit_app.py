import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="Painel BTC", layout="wide")
st.title("📊 Painel de Análise do Ciclo do Bitcoin")

# Seleção de datas
start = st.date_input("Data inicial", value=date(2021,1,1))
end = st.date_input("Data final", value=date.today())

# Download do preço
btc = yf.download("BTC-USD", start=start, end=end)

# Seletor de análise
analise = st.selectbox("Selecione o tipo de análise:", [
    "RSI Diário",
    "RSI Estocástico",
    "Fibonacci",
    "Média Móvel 200",
    "Comparar Ciclos"
])

# Gráfico básico
fig = go.Figure()
fig.add_trace(go.Scatter(x=btc.index, y=btc['Close'], name="BTC/USD"))

# Aplicação de análises básicas
if analise == "Média Móvel 200":
    btc['MM200'] = btc['Close'].rolling(window=200).mean()
    fig.add_trace(go.Scatter(x=btc.index, y=btc['MM200'], name="Média Móvel 200", line=dict(color="orange")))

# Exibe gráfico
st.plotly_chart(fig, use_container_width=True)

# Entrada de link externo
link = st.text_input("Cole aqui o link do gráfico externo (LookIntoBitcoin, Glassnode etc.)")

if st.button("Gerar Análise Simples"):
    st.success("📝 Análise baseada nos dados selecionados:")
    st.markdown(f"""
    - **Período:** {start} até {end}  
    - **Tipo de análise:** {analise}  
    - **Fonte externa:** {link if link else "Não informado"}  
    - **Resumo técnico (simulado):**  
        - Preço atual comparado à MM200 pode indicar fase de acumulação.
    """)
