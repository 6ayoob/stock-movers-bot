import logging
import pandas as pd
import yfinance as yf
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ التوكن الخاص بك
TELEGRAM_BOT_TOKEN = "7863509137:AAHBuRbtzMAOM_yBbVZASfx-oORubvQYxY8"

# ✅ قائمة المعرفات المسموح بها
ALLOWED_USERS = [
    5862477200, 5235493993, 5102764317, 5142531644,
    6060917300, 6557278187, 5053954152, 7863509137
]

# إعدادات اللوق
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ دالة التحقق من المستخدم
def is_allowed(user_id):
    return user_id in ALLOWED_USERS

# ✅ أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("🚫 غير مصرح لك باستخدام هذا البوت.")
        return
    await update.message.reply_text("✅ أهلاً بك! أرسل /scan للحصول على أفضل الأسهم من السوق.")

# ✅ أمر /scan لفحص السوق
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("🚫 غير مصرح لك باستخدام هذا البوت.")
        return

    await update.message.reply_text("🔍 جاري تحليل الأسهم، انتظر قليلاً...")
    try:
        symbols = []
        with open("symbols.txt", "r") as f:
            symbols = [line.strip() for line in f.readlines() if line.strip()]

        results = []
        for symbol in symbols:
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period="60d")
                if len(hist) < 50:
                    continue

                price = hist["Close"].iloc[-1]
                ma50 = hist["Close"].rolling(window=50).mean().iloc[-1]
                volume = hist["Volume"].iloc[-1]
                volume_avg = hist["Volume"].rolling(window=50).mean().iloc[-1]

                if price < 20 and price > ma50 and volume > volume_avg:
                    results.append(f"{symbol} - ${price:.2f} ✅")

            except Exception as e:
                logger.warning(f"تعذر تحليل السهم {symbol}: {e}")

        if results:
            message = "📈 أفضل الأسهم حسب الشروط:
\n" + "\n".join(results[:10])
        else:
            message = "❌ لا توجد أسهم تطابق الشروط حالياً."

        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {e}")

# ✅ تشغيل البوت
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))

    app.run_polling()

if __name__ == "__main__":
    main()
