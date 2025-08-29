import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "خلي هنا توكن بوتك"
CHANNEL_USERNAME = "@معرف قناتك" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_subscribed(update, context):
        await update.message.reply_text(
            f"⚠️ حتى تقدر تستخدم البوت، اشترك أولًا بالقناة: {CHANNEL_USERNAME}"
        )
        return

    await update.message.reply_text("اهلابيك حبيبي في بوت احمد خان!🌟\nأرسل لي رابط الفيديو من أي منصة وأنا أحمله إلك!")

async def is_subscribed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"خطأ أثناء التحقق من الاشتراك: {e}")
        return False

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

async def download_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_subscribed(update, context):
        await update.message.reply_text(
            f"⚠️ حتى تقدر تستخدم البوت، اشترك أولًا بالقناة: {CHANNEL_USERNAME}"
        )
        return

    url = update.message.text
    await update.message.reply_text("⏳ جاري التحميل، انتظر شوي...")

    try:
       
        filename = download_video(url)
        await update.message.reply_text("✅ تم التحميل! جاري الإرسال...")

       
        with open(filename, "rb") as video:
            await update.message.reply_video(video)

       
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ صار خطأ أثناء التحميل: {str(e)}")

if not os.path.exists("downloads"):
    os.makedirs("downloads")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_handler))

print("🚀 البوت يشتغل...")
app.run_polling()