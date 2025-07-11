import logging
import pandas as pd
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the bot token from environment variable
TOKEN = os.environ.get('BOT_TOKEN')

# Allowed username
ALLOWED_USERNAME = 'tayoob07_bot'

# Example function to fetch stock data (dummy implementation)
def get_stock_movers():
    data = {
        'Symbol': ['AAPL', 'TSLA', 'AMZN'],
        'Price': [150.25, 720.12, 3345.55],
        'Change': [1.5, -2.3, 0.8]
    }
    df = pd.DataFrame(data)
    return df

# Start command handler
def start(update: Update, context: CallbackContext):
    if update.effective_user.username != ALLOWED_USERNAME:
        update.message.reply_text("🚫 غير مصرح لك باستخدام هذا البوت.")
        return
    update.message.reply_text('مرحباً! أرسل /movers للحصول على تحركات السوق.')

# Movers command handler
def movers(update: Update, context: CallbackContext):
    if update.effective_user.username != ALLOWED_USERNAME:
        update.message.reply_text("🚫 غير مصرح لك باستخدام هذا البوت.")
        return
    df = get_stock_movers()
    message = "📈 تحركات السوق:\n\n"
    for _, row in df.iterrows():
        message += f"{row['Symbol']}: ${row['Price']} ({row['Change']}%)\n"
    update.message.reply_text(message)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("movers", movers))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
