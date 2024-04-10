import yfinance as yf
from prophet import Prophet
import pandas as pd
from datetime import datetime, timedelta

# Mengambil data historis harga saham dari Yahoo Finance
def fetch_stock_data(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        return data
    except Exception as e:
        print("Error:", e)
        return None

# Mengubah format data ke DataFrame untuk digunakan oleh Prophet
def prepare_data_for_prophet(data):
    if data is None or data.empty:
        return None
    df = data.reset_index()
    df.rename(columns={'Date':'ds', 'Open':'y'}, inplace=True) # Mengubah nama kolom sesuai dengan format Prophet
    return df[['ds', 'y']]

# Membuat prediksi menggunakan Prophet
def make_forecast(data):
    if data is None or data.empty:
        return None
    model = Prophet(daily_seasonality=True) # Menggunakan model Prophet dengan komponen musiman harian
    model.fit(data)

    # Membuat DataFrame untuk 5 hari ke depan
    future = model.make_future_dataframe(periods=10)
    
    # Melakukan prediksi
    forecast = model.predict(future)
    return forecast

# Fungsi untuk mencari data yang tersedia hingga tanggal tertentu
def find_available_data(symbol, end_date, days_back=10):
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    start_date = end_date - timedelta(days=days_back)
    data = fetch_stock_data(symbol, start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))
    return data




# Main function
def main():
    # Tentukan simbol saham dan tanggal hari ini
    symbol = 'SSIA.JK'  # Contoh: Apple (AAPL)
    # today = datetime.now().strftime('%Y-%m-%d')
    today = '2024-03-10'

    # Mencari data yang tersedia hingga tanggal hari ini
    stock_data = find_available_data(symbol, end_date=today)
    
    if stock_data is None:
        print("Data tidak tersedia.")
        return

    # Persiapkan data untuk model Prophet
    prophet_data = prepare_data_for_prophet(stock_data)
    
    if prophet_data is None or len(prophet_data) < 2:
        print("Data tidak cukup untuk prediksi.")
        return
    
    # Membuat prediksi menggunakan Prophet
    forecast = make_forecast(prophet_data)
    
    if forecast is None:
        print("Gagal membuat prediksi.")
        return
    
    # Menampilkan hasil prediksi
    forecasted_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(5)
    print("Prediksi harga saham untuk 5 hari ke depan:")
    print(forecasted_data)

if __name__ == "__main__":
    main()
