import requests
from bs4 import BeautifulSoup
import time
import os
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

load_dotenv()

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)
import os
import time
import logging
import requests
import threading
import schedule
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
STATUS_INTERVAL_HOURS = int(os.getenv("STATUS_INTERVAL_HOURS", "3"))

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# URL to check for tickets
TICKET_URL = "https://go.narcofest.ru/archstoyanie"

# Global state
last_check_time = None
last_check_result = None
bot_active = True

async def send_telegram_message(message):
    """Send a message via Telegram."""
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")

async def send_controls():
    """Send a message with control buttons."""
    bot = Bot(token=TELEGRAM_TOKEN)
    keyboard = [
        [
            InlineKeyboardButton("Check Now", callback_data="check_now"),
            InlineKeyboardButton("Status", callback_data="status"),
        ],
        [
            InlineKeyboardButton("Pause Bot", callback_data="pause"),
            InlineKeyboardButton("Resume Bot", callback_data="resume"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await bot.send_message(
        chat_id=CHAT_ID,
        text="Arch Ticket Hunter Controls:",
        reply_markup=reply_markup
    )

def check_tickets():
    """Check if tickets are available."""
    global last_check_time, last_check_result
    
    try:
        response = requests.get(TICKET_URL)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Look for sold out indicators
        sold_out_elements = soup.find_all(string=lambda text: "sold out" in text.lower() if text else False)
        ticket_available = len(sold_out_elements) == 0
        
        last_check_time = datetime.now()
        last_check_result = ticket_available
        
        return ticket_available
    except Exception as e:
        logger.error(f"Error checking tickets: {e}")
        last_check_time = datetime.now()
        last_check_result = None
        return None

async def send_status_report():
    """Send a status report via Telegram."""
    if not bot_active:
        return
    
    status = check_tickets()
    
    if status is None:
        message = "⚠️ <b>Status Report:</b> Error checking ticket availability."
    elif status:
        message = "🎉 <b>Status Report:</b> Tickets are AVAILABLE! Go buy them now!"
    else:
        message = "ℹ️ <b>Status Report:</b> No tickets available at this time."
    
    if last_check_time:
        message += f"\nLast checked: {last_check_time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    await send_telegram_message(message)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Welcome to Arch Ticket Hunter Bot! I'll check for ticket availability and notify you."
    )
    await send_controls()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = (
        "Arch Ticket Hunter Bot Commands:\n\n"
        "/start - Start the bot and show control buttons\n"
        "/status - Check current ticket status\n"
        "/controls - Show control buttons\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(help_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a status report when the command /status is issued."""
    await send_status_report()

async def controls_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send control buttons when the command /controls is issued."""
    await send_controls()

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses."""
    global bot_active
    
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_now":
        await query.edit_message_text(text="Checking for tickets now...")
        status = check_tickets()
        
        if status is None:
            message = "⚠️ Error checking ticket availability."
        elif status:
            message = "🎉 Tickets are AVAILABLE! Go buy them now!"
        else:
            message = "ℹ️ No tickets available at this time."
        
        await query.edit_message_text(text=message)
        await send_controls()
    
    elif query.data == "status":
        await query.edit_message_text(text="Fetching status...")
        await send_status_report()
        await send_controls()
    
    elif query.data == "pause":
        bot_active = False
        await query.edit_message_text(text="Bot paused. Automatic checks are disabled.")
        await send_controls()
    
    elif query.data == "resume":
        bot_active = True
        await query.edit_message_text(text="Bot resumed. Automatic checks are enabled.")
        await send_controls()

def run_schedule():
    """Run the scheduler in the background."""
    while True:
        schedule.run_pending()
        time.sleep(1)

async def scheduled_status_report():
    """Function to be called by the scheduler."""
    await send_status_report()

def main():
    """Start the bot."""
    # Set up the Telegram application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("controls", controls_command))
    
    # Add callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Schedule regular status reports every 3 hours
    interval_hours = STATUS_INTERVAL_HOURS
    for hour in range(0, 24, interval_hours):
        schedule.every().day.at(f"{hour:02d}:00").do(
            lambda: asyncio.run(scheduled_status_report())
        )
    
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_schedule)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Send initial message
    asyncio.run(send_telegram_message("🤖 Arch Ticket Hunter Bot started!"))
    asyncio.run(send_controls())
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    import asyncio
    main()
def keep_alive():
    t = Thread(target=run)
    t.start()

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
    time.sleep(75)