import telebot
from apis import *
import google.generativeai as gemini
import webbrowser
import platform
import os
import random

bot = telebot.TeleBot(API_KEY_TELEGRAM)
gemini.configure(api_key=GEMINI_API_KEY)
model = gemini.GenerativeModel('gemini-pro')

def create_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    chrome_button = telebot.types.KeyboardButton('Abrir Chrome')
    github_button = telebot.types.KeyboardButton('Abrir Github')
    brightness_button = telebot.types.KeyboardButton('Ajustar Brilho')
    markup.add(chrome_button, brightness_button, github_button)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = create_markup()
    bot.send_message(message.chat.id, "Escolha uma opção:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Abrir Chrome')
def open_chrome(message):
    url = 'https://google.com'
    webbrowser.open(url)
    bot.send_message(message.chat.id, "Chrome aberto.")


@bot.message_handler(func=lambda message: message.text == 'Abrir Github')
def open_chrome(message):
    url = 'https://github.com'
    webbrowser.open(url)
    bot.send_message(message.chat.id, "Chrome aberto."
@bot.message_handler(func=lambda message: message.text == 'Ajustar Brilho')
def adjust_brightness(message):
    levels = [15, 50, 90]
    level = random.choice(levels)

    try:
        if platform.system() == "Windows":
            os.system(f"powershell (Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})")
            bot.send_message(message.chat.id, f"Brilho ajustado para {level}%.")
        else:
            bot.reply_to(message, "Ajuste de brilho não suportado neste sistema.")
    except Exception as e:
        bot.reply_to(message, f"{str(e)}")

@bot.message_handler(func=lambda message: True)
def response(message):
    try:
        response = model.generate_content(prompt=message.text)
        text_response = response.candidates[0].text
        bot.reply_to(message, text_response)
    except Exception as e:
        bot.reply_to(message, f" {str(e)}")

# Inicia o bot
bot.polling()
