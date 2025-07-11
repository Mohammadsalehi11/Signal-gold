import requests
import time
import yfinance as yf
import numpy as np

=== تنظیمات اولیه ===

TELEGRAM_TOKEN = "7768350914:AAEsyVuKXGWT9PuzcThKb1Cjp6sNxtPPU1g"
CHAT_ID = "7261157918"
SYMBOL = "XAUUSD=X"  # طلای جهانی در Yahoo Finance
INTERVAL = "5m"      # تایم فریم ۵ دقیقه

=== توابع کمکی ===

def send_telegram_message(text):
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
requests.post(url, data=data)

def compute_rsi(data, period=14):
delta = np.diff(data)
gain = np.where(delta > 0, delta, 0)
loss = np.where(delta < 0, -delta, 0)
avg_gain = np.convolve(gain, np.ones(period)/period, mode='valid')
avg_loss = np.convolve(loss, np.ones(period)/period, mode='valid')
rs = avg_gain / (avg_loss + 1e-10)
rsi = 100 - (100 / (1 + rs))
return np.concatenate((np.full(period, np.nan), rsi))

def compute_ema(data, period=20):
ema = []
k = 2 / (period + 1)
for i in range(len(data)):
if i == 0:
ema.append(data[0])
else:
ema.append(data[i]k + ema[i-1](1-k))
return np.array(ema)

def find_support_resistance(prices, window=20):
supports = []
resistances = []
for i in range(window, len(prices)-window):
local_min = min(prices[i-window:i+window])
local_max = max(prices[i-window:i+window])
if prices[i] == local_min:
supports.append(prices[i])
if prices[i] == local_max:
resistances.append(prices[i])
# میانگین حمایت و مقاومت برای ساده سازی
support = np.mean(supports) if supports else prices[-1]
resistance = np.mean(resistances) if resistances else prices[-1]
return support, resistance

def fetch_data():
df = yf.download(tickers=SYMBOL, period="1d", interval=INTERVAL)
close_prices = df['Close'].values
return close_prices

def analyze_and_signal():
close = fetch_data()
if len(close) < 40:
print("دیتا کافی نیست")
return

rsi = compute_rsi(close)[-1]  
ema = compute_ema(close)[-1]  
price = close[-1]  
support, resistance = find_support_resistance(close)  

# شرایط سیگنال خرید  
buy_cond = (rsi < 30) and (price > ema) and (abs(price - support) / support < 0.01)  
# شرایط سیگنال فروش  
sell_cond = (rsi > 70) and (price < ema) and (abs(price - resistance) / resistance < 0.01)  

if buy_cond:  
    entry = price  
    take_profit = entry + 20  
    stop_loss = entry - 15  
    msg = f"📢 *سیگنال خرید طلای جهانی*\n\n"\  
          f"📌 قیمت فعلی: {entry:.2f}\n"\  
          f"🟢 RSI = {rsi:.2f} (اشباع فروش)\n"\  
          f"📉 حمایت: {support:.2f}\n"\  
          f"📈 روند مثبت (EMA20 = {ema:.2f})\n\n"\  
          f"🎯 ورود: {entry:.2f}\n"\  
          f"🎯 حد سود: {take_profit:.2f}\n"\  
          f"⛔ حد ضرر: {stop_loss:.2f}"  
    send_telegram_message(msg)  
    print("سیگنال خرید ارسال شد")  

elif sell_cond:  
    entry = price  
    take_profit = entry - 20  
    stop_loss = entry + 15  
    msg = f"📢 *سیگنال فروش طلای جهانی*\n\n"\  
          f"📌 قیمت فعلی: {entry:.2f}\n"\  
          f"🔴 RSI = {rsi:.2f} (اشباع خرید)\n"\  
          f"📈 مقاومت: {resistance:.2f}\n"\  
          f"📉 روند منفی (EMA20 = {ema:.2f})\n\n"\  
          f"🎯 ورود: {entry:.2f}\n"\  
          f"🎯 حد سود: {take_profit:.2f}\n"\  
          f"⛔ حد ضرر: {stop_loss:.2f}"  
    send_telegram_message(msg)  
    print("سیگنال فروش ارسال شد")  
else:  
    print("فعلا سیگنال معتبر نیست")

if name == "main":
while True:
try:
analyze_and_signal()
except Exception as e:
print("خطا:", e)
time.sleep(60)

