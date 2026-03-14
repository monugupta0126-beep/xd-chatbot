import telebot
from flask import Flask, request

# Configuration
BOT_TOKEN = '8733278178:AAHQYFwsjHup-rFirUk54Ay4QjRBGnVcizs'
ADMIN_ID = 8772214154
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

# Webhook route
@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    return "Bot is Running on Vercel!", 200

# Bot Commands
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! Main Vercel par live hoon. 😊")

@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def forward_to_admin(message):
    try:
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    except: pass

@bot.message_handler(func=lambda message: message.reply_to_message is not None and message.chat.id == ADMIN_ID)
def reply_to_user(message):
    try:
        # Vercel par database nahi hota, isliye forward_from privacy depend karti hai
        if message.reply_to_message.forward_from:
            target_id = message.reply_to_message.forward_from.id
            bot.copy_message(target_id, ADMIN_ID, message.message_id)
        else:
            bot.reply_to(message, "❌ User ki privacy ON hai, reply nahi ja sakta.")
    except: pass
