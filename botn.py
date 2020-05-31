import telebot
from telebot import types
import random
from datetime import datetime

bot = telebot.TeleBot('''Bot ID''')
telebot.apihelper.proxy = {'''Your proxy'''}

@bot.message_handler(commands = ['start'])
def welcome(message):
    sti = open('hi.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рандомное число")
    item2 = types.KeyboardButton("Хочу новые обои")
    item3 = types.KeyboardButton("Сколько время?")
            
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот с лучшими обоями.'.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types = ['text'])
def get_text_message(message):
        if message.chat.type == 'private':
            if message.text == "Рандомное число":
                bot.send_message(message.chat.id, str(random.randint(0, 100)))
            elif message.text == 'Сколько время?':
                time = datetime.now().strftime('%H+3:%M:%S')
                bot.send_message(message.chat.id, 'Сейчас '+time)
            elif message.text == 'Хочу новые обои':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("1080x1920", callback_data='small')
                item2 = types.InlineKeyboardButton("1440x2560", callback_data='big')

                markup.add(item1, item2)
                print(message.chat.first_name, message.chat.last_name)
                print(message.chat.username)
                print(message.chat.id)
                bot.send_message(message.chat.id, 'Какого разрешения?', reply_markup=markup)
            elif message.text == 'Рассылка' and message.chat.id == adminChat:
                bot.send_message(message.chat.id, 'Введите текст рассылки')

            elif message.chat.id == adminChat: 
                bot.send_message(message.chat.id, 'Здравствуйте, господин')

            else:
                bot.send_message(message.chat.id, 'Не знаю, что ответить.')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'small':
                num = str(random.randint(1, 91))
                photo = open('wallpapers/smartphone/small/'+num+'.jpg', 'rb')
                bot.send_chat_action(call.message.chat.id, action='upload_photo')
                bot.send_document(call.message.chat.id, photo)
            elif call.data == 'big':
                num = str(random.randint(1, 25))
                photo = open('wallpapers/smartphone/big/'+num+'.jpg', 'rb')
                bot.send_chat_action(call.message.chat.id, action='upload_photo')
                bot.send_document(call.message.chat.id, photo)
    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)