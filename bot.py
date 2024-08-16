import config
import random
from random import choice
import telebot
from telebot import types

API_TOKEN = config.token

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add(types.KeyboardButton('камень'), types.KeyboardButton('ножницы'), types.KeyboardButton('бумага'))
    bot.reply_to(message, "Добро пожаловать в игру 'Камень, ножницы, бумага'! Для игры используйте кнопки ниже:", reply_markup=markup)

def is_user_admin(chat_id, user_id): 
    chat_member = bot.get_chat_member(chat_id, user_id) 
    return chat_member.status == "administrator" or chat_member.status == "creator" 


@bot.message_handler(func=lambda message: True)
def play_game(message):
    user_choice = message.text
    bot_choice = random.choice(['камень', 'ножницы', 'бумага'])

    if user_choice not in ['камень', 'ножницы', 'бумага']:
        return
    if user_choice == bot_choice:
        bot.reply_to(message, f"Вы выбрали {user_choice}, а я выбрал {bot_choice}. Ничья!")
    elif (user_choice == 'камень' and bot_choice == 'ножницы') or (user_choice == 'ножницы' and bot_choice == 'бумага') or (user_choice == 'бумага' and bot_choice == 'камень'):
        bot.reply_to(message, f"Вы выбрали {user_choice}, а я выбрал {bot_choice}. Вы победили!")
    else:
        bot.reply_to(message, f"Вы выбрали {user_choice}, а я выбрал {bot_choice}. Я победил! ")

bot.polling()



@bot.message_handler(commands=['ban'])
def echo_message(message):
  
    chat_id = message.chat.id 
    user_id = message.from_user.id 

    if is_user_admin(chat_id, user_id): 
        try: 
            user_to_ban = message.reply_to_message.from_user.id 
            bot.kick_chat_member(chat_id, user_to_ban) 
            bot.reply_to(message, "Пользователь забанен.") 
        except Exception as e: 
            bot.reply_to(message, "Не удалось забанить пользователя.") 
    else: 
        bot.reply_to(message, "У вас нет прав для этой команды.") 

bot.infinity_polling(none_stop=True)



