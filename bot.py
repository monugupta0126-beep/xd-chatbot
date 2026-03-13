import telebot
import os
from flask import Flask
from threading import Thread
import random
import string

# 1. Flask Server (Render ke liye)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Living with Video Call Feature!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Bot Configuration
BOT_TOKEN = '8733278178:AAHQYFwsjHup-rFirUk54Ay4QjRBGnVcizs'
ADMIN_ID = 8772214154 
bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# Unique Room ID banane ke liye function
def generate_room_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! Main active hoon. Video Call ke liye admin ko request karein. 😊")

# 3. User ka message Admin ko bhejna
@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID, 
                     content_types=['text', 'photo', 'sticker', 'video', 'voice'])
def forward_to_admin(message):
    try:
        forwarded_msg = bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        user_data[forwarded_msg.message_id] = message.chat.id
    except Exception as e:
        print(f"Forward Error: {e}")

# 4. Admin ka Reply aur Special Video Call Command
@bot.message_handler(func=lambda message: message.reply_to_message is not None and message.chat.id == ADMIN_ID,
                     content_types=['text', 'photo', 'sticker', 'video', 'voice'])
def reply_to_user(message):
    try:
        reply_to_id = message.reply_to_message.message_id
        
        # User ID dhoondna
        if reply_to_id in user_data:
            target_user_id = user_data[reply_to_id]
        elif message.reply_to_message.forward_from:
            target_user_id = message.reply_to_message.forward_from.id
        else:
            bot.reply_to(message, "❌ User ID nahi mili.")
            return

        # AGAR ADMIN '/call' LIKHTA HAI
        if message.text and message.text.lower() == '/call':
            room_id = generate_room_id()
            call_link = f"https://meet.jit.si/{room_id}"
            
            # Admin ko link bhejna
            bot.send_message(ADMIN_ID, f"📞 **Video Call Link Taiyar Hai!**\n\nAap is par click karein:\n{call_link}", parse_mode="Markdown")
            
            # User ko link bhejna
            bot.send_message(target_user_id, f"👤 **Admin aapse Video Call karna chahte hain.**\n\nJoin karne ke liye niche link par click karein:\n{call_link}", parse_mode="Markdown")
            print(f"✅ Video Call link sent to {target_user_id}")
            
        else:
            # Normal Reply (Text, Sticker, etc.)
            bot.copy_message(target_user_id, ADMIN_ID, message.message_id)
            print(f"✅ Normal Reply sent to {target_user_id}")

    except Exception as e:
        print(f"Reply Error: {e}")

# 5. Main Execution
if __name__ == "__main__":
    keep_alive()
    print("Bot with Video Call is starting...")
    bot.infinity_polling()
