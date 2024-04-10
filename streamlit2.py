import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Fungsi untuk mengambil data saham
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Fungsi untuk membuat grafik pergerakan harga saham
def plot_stock_data(stock_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(stock_data['Close'], label='Close')
    ax.set_title('Pergerakan Harga Saham')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Harga (USD)')
    ax.legend()
    st.pyplot(fig)


# Fungsi untuk menghitung Moving Average (MA)
def calculate_ma(data, window=30):
    return data['Close'].rolling(window=window).mean()

# Fungsi untuk menghitung Exponential Moving Average (EMA)
def calculate_ema(data, window=20):
    return data['Close'].ewm(span=window, adjust=False).mean()

# Fungsi untuk menghitung Stochastic Oscillator
def calculate_stochastic_oscillator(data):
    low_min = data['Low'].rolling(window=14).min()
    high_max = data['High'].rolling(window=14).max()
    data['%K'] = (data['Close'] - low_min) / (high_max - low_min) * 100
    data['%D'] = data['%K'].rolling(window=3).mean()
    return data[['%K', '%D']]

# Main function
def main():
    st.title('Aplikasi Data Saham')

    # Input ticker saham dan tahun
    ticker = st.text_input('Masukkan Ticker Saham (Contoh: AAPL untuk Apple Inc.)', 'AAPL')
    year = st.slider('Pilih Tahun', min_value=2010, max_value=2024, value=2020)

    # Mendapatkan data saham
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'
    stock_data = get_stock_data(ticker, start_date, end_date)

    if stock_data.empty:
        st.warning('Data saham tidak tersedia. Mohon periksa kembali ticker saham yang dimasukkan.')
    else:
        # Menampilkan data saham
        st.subheader('Data Saham')
        st.write(stock_data)

        # Menampilkan grafik pergerakan harga saham
        st.subheader('Grafik Pergerakan Harga Saham')
        plot_stock_data(stock_data)

        # Menampilkan indikator tambahan
        st.subheader('Indikator Tambahan')
        st.write('**Moving Average (30):**', calculate_ma(stock_data)[-1])
        st.write('**Exponential Moving Average (20):**', calculate_ema(stock_data)[-1])

        stochastic_data = calculate_stochastic_oscillator(stock_data)
        st.write('**Stochastic Oscillator (%K):**', stochastic_data['%K'].iloc[-1])
        st.write('**Stochastic Oscillator (%D):**', stochastic_data['%D'].iloc[-1])

if __name__ == '__main__':
    main()
