import telebot

BOT_TOKEN = "8276024070:AAGmFapEgRTJPnrLKAH2ybrozPAN-ZPRpJI"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda m: True)
def get_id(message):
    print("CHAT ID:", message.chat.id)
        bot.reply_to(message, f"Chat ID: {message.chat.id}")

        bot.infinity_polling()