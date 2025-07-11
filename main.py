import logging
import os
import yfinance as yf
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# إعداد البوت
  TELEGRAM_BOT_TOKEN = "6940662750:AAGDKoZtIA8-eTIYogEA6kp0DGt0OVp95e4"

# ثم في دالة main:
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()


# السجل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرسل /stock <رمز السهم> للحصول على سعره.")

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("الرجاء إدخال رمز السهم مثل: /stock AAPL")
        return
    symbol = context.args[0].upper()
    try:
        data = yf.Ticker(symbol)
        price = data.info['regularMarketPrice']
        name = data.info.get('shortName', symbol)
        await update.message.reply_text(f"📈 {name} ({symbol})\nالسعر الحالي: ${price}")
    except Exception as e:
        await update.message.reply_text("حدث خطأ. تأكد من رمز السهم وأعد المحاولة.")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(  "123456789:ABCdefGHIjklMNOpqrSTUvwxYZ12345678"
).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stock", stock))
    app.run_polling()
