import requests
import pandas as pd
import time

TOKEN = '7768350914:AAEsyVuKXGWT9PuzcThKb1Cjp6sNxtPPU1g'
CHAT_ID = '7261157918'

def send_signal(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def fetch_price_data():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/XAUUSD=X?range=1d&interval=5m"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    try:
        data = response.json()
        timestamps = data['chart']['result'][0]['timestamp']
        prices = data['chart']['result'][0]['indicators']['quote'][0]['close']
        df = pd.DataFrame({'time': timestamps, 'close': prices})
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df.dropna()
    except:
        return None

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def check_signal():
    df = fetch_price_data()
    if df is None or df.empty:
        return
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['RSI'] = compute_rsi(df['close'])
    last = df.iloc[-1]
    price = round(last['close'], 2)
    rsi = round(last['RSI'], 2)
    ema = round(last['EMA20'], 2)
    if rsi < 30 and price > ema:
        tp = round(price + 15, 2)
        sl = round(price - 20, 2)
        text = f"ورود {price}\nحد سود {tp}\nحد ضرر {sl}"
        send_signal(text)

if __name__ == "__main__":
    while True:
        check_signal()
        time.sleep(900)
