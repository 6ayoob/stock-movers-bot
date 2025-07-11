import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scanner import scan_stocks
import asyncio
import datetime

# ✅ التوكن الخاص بك
TELEGRAM_BOT_TOKEN = "7863509137:AAEmoyimZV-XVHcA7aBT15e4IRoxB9WR0hY"

# ✅ قائمة المعرفات المسموح بها
ALLOWED_USERS = [
    7863509137, 5862477200, 5235493993, 5102764317,
    5142531644, 6060917300, 6557278187, 5053954152
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
        return await update.message.reply_text("🚫 غير مصرح لك باستخدام هذا البوت.")
    await update.message.reply_text("✅ أهلاً بك! أرسل /scan للحصول على أفضل الأسهم.")

# ✅ أمر /scan
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        return await update.message.reply_text("🚫 غير مصرح لك باستخدام هذا البوت.")

    await update.message.reply_text("🔍 يتم الآن فحص السوق...")
    results = scan_stocks()

    if not results:
        await update.message.reply_text("❌ لم يتم العثور على أسهم مطابقة.")
        return

    msg = "📈 أفضل الأسهم (سعر < 20$):\n\n"
    for symbol, price, volume in results:
        msg += f"{symbol}: ${price:.2f} | حجم: {volume:,}\n"

    await update.message.reply_text(msg)

# ✅ مهمة إرسال التقرير اليومي
async def send_daily_report(application):
    while True:
        now = datetime.datetime.now()
        target = now.replace(hour=15, minute=0, second=0, microsecond=0)
        if now > target:
            target += datetime.timedelta(days=1)

        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        results = scan_stocks()
        msg = "📊 تقرير الأسهم اليومية:\n\n"
        if not results:
            msg += "❌ لم يتم العثور على أسهم مطابقة اليوم."
        else:
            for symbol, price, volume in results:
                msg += f"{symbol}: ${price:.2f} | حجم: {volume:,}\n"

        for user_id in ALLOWED_USERS:
            try:
                await application.bot.send_message(chat_id=user_id, text=msg)
            except Exception as e:
                logger.warning(f"فشل إرسال الرسالة إلى {user_id}: {e}")

# ✅ تشغيل البوت
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))

    # إرسال تقرير تلقائي
    app.create_task(send_daily_report(app))

    app.run_polling()

if __name__ == "__main__":
    main()
