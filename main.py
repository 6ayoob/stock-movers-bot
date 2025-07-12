import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yfinance as yf
import datetime
import pytz
import asyncio
import pandas as pd

# إعدادات البوت
TELEGRAM_BOT_TOKEN = "7863509137:AAHBuRbtzMAOM_yBbVZASfx-oORubvQYxY8"
ALLOWED_USERS = [7863509137]
REPORT_TIME_HOUR = 15  # الساعة 3 مساءً بتوقيت السعودية

# إعدادات اللوق
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# تحميل قائمة الأسهم من ملف
def load_symbols():
    with open("symbols.txt", "r") as f:
        return [line.strip().upper() for line in f.readlines() if line.strip()]

# التحقق من المستخدم
def is_allowed(user_id):
    return user_id in ALLOWED_USERS

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("🚫 غير مصرح لك باستخدام هذا البوت.")
        return
    await update.message.reply_text("✅ أهلاً بك! أرسل /scan للحصول على أفضل الأسهم.")

# فحص الأسهم
def scan_stocks():
    symbols = load_symbols()
    good_stocks = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="3mo")
            if df.empty or len(df) < 50:
                continue

            df["50ma"] = df["Close"].rolling(window=50).mean()
            df["50vol"] = df["Volume"].rolling(window=50).mean()
            latest = df.iloc[-1]

            if (
                latest["Close"] < 20 and
                latest["Close"] > latest["50ma"] and
                latest["Volume"] > latest["50vol"]
            ):
                name = ticker.info.get("shortName", symbol)
                good_stocks.append(f"📈 {name} ({symbol})\nالسعر: ${latest['Close']:.2f}")

        except Exception:
            continue

    if not good_stocks:
        return "❌ لم يتم العثور على أسهم مطابقة للشروط."
    return "\n\n".join(good_stocks[:10])  # نرسل أول 10 فقط

# أمر /scan
async def scan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("🚫 غير مصرح لك باستخدام هذا البوت.")
        return

    await update.message.reply_text("🔍 جاري فحص السوق...")
    result = await asyncio.to_thread(scan_stocks)
    await update.message.reply_text(result)

# إرسال التقرير اليومي التلقائي
async def daily_report(app):
    while True:
        now = datetime.datetime.now(pytz.timezone("Asia/Riyadh"))
        if now.hour == REPORT_TIME_HOUR and now.minute == 0:
            result = await asyncio.to_thread(scan_stocks)
            for user_id in ALLOWED_USERS:
                try:
                    await app.bot.send_message(chat_id=user_id, text="📊 تقرير السوق اليومي:\n\n" + result)
                except Exception as e:
                    logger.error(f"فشل في إرسال التقرير إلى {user_id}: {e}")
            await asyncio.sleep(60)
        await asyncio.sleep(30)

# تشغيل البوت
async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan_command))

    app.create_task(daily_report(app))

    await app.run_polling()


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print("تم إيقاف البوت يدويًا")
        sys.exit()
