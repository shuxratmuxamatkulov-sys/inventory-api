import os
import requests
import telebot

# Bot tokeningizni kiriting
BOT_TOKEN = "8816399892:AAHfp_7lfvB1h781FEOsccNoOy4Z6DnLdII"
# Railway-dagi backend manzilingiz
API_BASE_URL = "https://inventory-api-production-b472.up.railway.app/api"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"Assalomu alaykum, {message.from_user.first_name}!\n"
        "Fen Textile ombor va mahsulotlar hisobi botiga xush kelibsiz.\n\n"
        "Mavjud buyruqlar:\n"
        "/products - Ombor mahsulotlari ro'yxati\n"
        "/categories - Kategoriyalar ro'yxati"
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['products'])
def get_products(message):
    try:
        response = requests.get(f"{API_BASE_URL}/products/")
        if response.status_code == 200:
            products = response.json()
            if not products:
                bot.reply_to(message, "📦 Omborda hozircha mahsulotlar mavjud emas.")
                return

            text = "📦 **Ombordagi mahsulotlar:**\n\n"
            for item in products:
                # API qaytarayotgan maydon nomlariga qarab moslang
                name = item.get('name', 'Nomsiz')
                quantity = item.get('quantity', 0)
                text += f"• **{name}**: {quantity} ta/kg\n"

            bot.reply_to(message, text, parse_mode="Markdown")
        else:
            bot.reply_to(message, f"⚠️ Xatolik kodi: {response.status_code}\n{response.text}")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Server bilan aloqa o'rnatib bo'lmadi: {str(e)}")


if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.polling(none_stop=True)