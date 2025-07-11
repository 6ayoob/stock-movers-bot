
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yfinance as yf

# ✅ التوكن الخاص بك
TELEGRAM_BOT_TOKEN = "6940662750:AAGDKoZtIA8-eTIYogEA6kp0DGt0OVp95e4"

# ✅ قائمة المعرفات المسموح بها
ALLOWED_USERS = [
    5862477200, 5235493993, 5102764317, 5142531644,
    6060917300, 6557278187, 5053954152
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
    await update.message.reply_text("✅ أهلاً بك! أرسل الأمر /stock مع رمز السهم مثل /stock AAPL")

# ✅ أمر /stock لعرض سعر السهم
async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("🚫 غير مصرح لك باستخدام هذا البوت.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("❌ الرجاء كتابة رمز السهم بشكل صحيح. مثال: /stock AAPL")
        return

    symbol = context.args[0].upper()
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.info["regularMarketPrice"]
        name = ticker.info.get("shortName", symbol)
        await update.message.reply_text(f"💹 {name} ({symbol})\nالسعر الحالي: ${price}")
    except Exception as e:
        await update.message.reply_text(f"❌ لم أتمكن من جلب بيانات {symbol}.\n{e}")

# ✅ إنشاء البوت
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stock", stock))

    app.run_polling()

if __name__ == "__main__":
    main()
