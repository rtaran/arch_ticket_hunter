import requests
from bs4 import BeautifulSoup
import time
import os

# URL to check
URL = "https://tickets.stoyanie.ru/shop/vhodnoj-bilet-na-arhstoyanie-detskoe-2025-na-tryoh-chelovek/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Environment variables (set in Replit Secrets tab)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"❌ Telegram error: {e}")

def check_ticket():
    try:
        response = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        button = soup.find("button", {"class": "single_add_to_cart_button"})
        if button:
            print("🎉 БИЛЕТ ДОСТУПЕН!")
            send_telegram_message("🎉 БИЛЕТ НА АРХСТОЯНИЕ ДОСТУПЕН! 👉 " + URL)
        else:
            print("⏳ Пока нет билетов...")
    except Exception as e:
        print(f"Ошибка: {e}")

# Repeat check every 5 minutes
while True:
    check_ticket()
    time.sleep(300)