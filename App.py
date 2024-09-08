import telebot
from apis import *
import google.generativeai as gemini
import webbrowser

bot = telebot.TeleBot(API_KEY_TELEGRAM)
gemini.configure(api_key= GEMINI_API_KEY)
model = gemini.GenerativeModel('gemini-pro')


def verify(message):
    return True


@bot.message_handler(func= verify)
def response(message):
        response = model.generate_content(message.text)
        text_response = response.candidates[0].content.parts[0].text
        bot.reply_to(message, text_response)





bot.polling()