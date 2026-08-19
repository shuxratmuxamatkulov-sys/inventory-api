from django.core.management.base import BaseCommand
import telebot
import requests

# Бот токени ва API URL
BOT_TOKEN = 'СИЗНИНГ_BOT_TOKENИНГИЗ'  # Шу ерга бот токенингизни ёзинг
API_URL = 'https://inventory-api-production-b472.up.railway.app/api/'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Fen Textile ombor va mahsulotlar hisobi botiga xush kelibsiz.\n\nMavjud buyruqlar:\n/products - Ombor mahsulotlari ro'yxati\n/categories - Kategoriyalar ro'yxati")

@bot.message_handler(commands=['products'])
def get_products(message):
    try:
        res = requests.get(f"{API_URL}products/")
        if res.status_code == 200 and res.json():
            products = res.json()
            text = "📦 **Ombordagi mahsulotlar:**\n\n"
            for p in products:
                text += f"🔹 **{p.get('name')}**: {p.get('quantity', 0)} ta ({p.get('price', 0)} so'm)\n"
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "📦 Omborda hozircha mahsulotlar mavjud emas.")
    except Exception as e:
        bot.send_message(message.chat.id, "Хатолик юз берди.")

@bot.message_handler(commands=['categories'])
def get_categories(message):
    try:
        res = requests.get(f"{API_URL}categories/")
        if res.status_code == 200 and res.json():
            cats = res.json()
            text = "📁 **Kategoriyalar:**\n\n"
            for c in cats:
                text += f"▪️ {c.get('name')}\n"
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "📁 Hozircha kategoriyalar mavjud emas.")
    except Exception as e:
        bot.send_message(message.chat.id, "Хатолик юз берди.")

class Command(BaseCommand):
    help = 'Telegram ботни ишга тушириш буйруғи'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Telegram bot ишга тушди..."))
        bot.infinity_polling()