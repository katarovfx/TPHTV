# import telebot
# bot = telebot.TeleBot('8201538144:AAGX48HY6FylnrncPsmzfUk9xS6nWTsRBhQ')

# @bot.message_handler(commands=["start"])
# def welcome(message):
#     bot.send_message(message.chat.id, "welcome to TPHTV ")


# bot.polling()
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تنظیم لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دیکشنری برای رمزنگاری (جابجایی حروف انگلیسی و فارسی)
CIPHER_MAP = {
    'a': 'p', 'b': 'o', 'c': 'n', 'd': 'm', 'e': 'l', 'f': 'k', 'g': 'j',
    'h': 'i', 'i': 'h', 'j': 'g', 'k': 'f', 'l': 'e', 'm': 'd', 'n': 'c',
    'o': 'b', 'p': 'a', 'q': 'z', 'r': 'y', 's': 'x', 't': 'w', 'u': 'v',
    'v': 'u', 'w': 't', 'x': 's', 'y': 'r', 'z': 'q',
    'ا': 'پ', 'ب': 'ت', 'پ': 'ث', 'ت': 'ج', 'ث': 'چ', 'ج': 'ح', 'چ': 'خ',
    'ح': 'د', 'خ': 'ذ', 'د': 'ر', 'ذ': 'ز', 'ر': 'ژ', 'ز': 'س', 'ژ': 'ش',
    'س': 'ص', 'ش': 'ض', 'ص': 'ط', 'ض': 'ظ', 'ط': 'ع', 'ظ': 'غ', 'ع': 'ف',
    'غ': 'ق', 'ف': 'ک', 'ق': 'گ', 'ک': 'ل', 'گ': 'م', 'ل': 'ن', 'م': 'و',
    'ن': 'ه', 'و': 'ی', 'ه': 'ا', 'ی': 'ب'
}

# دیکشنری معکوس برای رمزگشایی
DECIPHER_MAP = {value: key for key, value in CIPHER_MAP.items()}

def encrypt_message(text: str) -> str:
    """تبدیل پیام به پیام رمزی با جابجایی حروف"""
    result = ''
    for char in text:
        if char in CIPHER_MAP:
            result += CIPHER_MAP[char]
        else:
            result += char  # اگر حرف در دیکشنری نبود، بدون تغییر می‌ماند
    return result

def decrypt_message(text: str) -> str:
    """تبدیل پیام رمزی به پیام معمولی"""
    result = ''
    for char in text:
        if char in DECIPHER_MAP:
            result += DECIPHER_MAP[char]
        else:
            result += char  # اگر حرف در دیکشنری نبود، بدون تغییر می‌ماند
    return result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ارسال پیام خوش‌آمدگویی با کیبورد سفارشی"""
    keyboard = [['رمزنگاری', 'رمزگشایی']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text(
        'سلام! من یک ربات رمزنگاری هستم.\n'
        'لطفاً یکی از گزینه‌های «رمزنگاری» یا «رمزگشایی» را از کیبورد پایین انتخاب کنید و سپس پیام خود را بفرستید.',
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """مدیریت پیام‌های متنی و انجام رمزنگاری یا رمزگشایی"""
    user_message = update.message.text

    if user_message in ['رمزنگاری', 'رمزگشایی']:
        context.user_data['mode'] = 'encrypt' if user_message == 'رمزنگاری' else 'decrypt'
        mode_text = 'رمزنگاری' if user_message == 'رمزنگاری' else 'رمزگشایی'
        await update.message.reply_text(f'حالت {mode_text} انتخاب شد. حالا پیام خود را بفرستید.')
        return

    if 'mode' not in context.user_data:
        await update.message.reply_text('لطفاً ابتدا با انتخاب «رمزنگاری» یا «رمزگشایی» از کیبورد پایین، یک حالت انتخاب کنید.')
        return

    mode = context.user_data['mode']
    if mode == 'encrypt':
        result = encrypt_message(user_message)
        await update.message.reply_text(f'پیام رمزی: {result}')
    elif mode == 'decrypt':
        result = decrypt_message(user_message)
        await update.message.reply_text(f'پیام رمزگشایی‌شده: {result}')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """مدیریت خطاها"""
    logger.error(f'Update {update} caused error {context.error}')

def main() -> None:
    """راه‌اندازی ربات"""
    # استفاده از توکن ارائه‌شده
    application = Application.builder().token('8201538144:AAGX48HY6FylnrncPsmzfUk9xS6nWTsRBhQ').build()

    # افزودن هندلرها
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # شروع ربات
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()