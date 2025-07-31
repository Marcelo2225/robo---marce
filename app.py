import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

st.set_page_config(page_title="Robô Marce - Análise Gráfica", layout="wide")

st.title("📊 Robô Marce - Análise Gráfica em Tempo Real")

st.sidebar.header("Configuração de Indicadores")
rsi_period = st.sidebar.slider("Período do RSI", 2, 50, 14)
ma_period = st.sidebar.slider("Período da Média Móvel", 2, 100, 20)
symbol = st.sidebar.selectbox("Par de Moeda", ["EUR/USD", "GBP/USD", "AUD/CAD", "USD/JPY"])

# Simulação de dados
np.random.seed(42)
dates = pd.date_range(end=dt.datetime.now(), periods=100, freq='min')
prices = np.cumsum(np.random.randn(100)) + 100
df = pd.DataFrame({"Time": dates, "Price": prices})
df["MA"] = df["Price"].rolling(ma_period).mean()

def calculate_rsi(series, period):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df["RSI"] = calculate_rsi(df["Price"], rsi_period)

st.line_chart(df.set_index("Time")[["Price", "MA"]], height=300)
st.line_chart(df.set_index("Time")[["RSI"]], height=150)
