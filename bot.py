import telebot
from telebot import types
from datetime import datetime
import config, threading, data_manager, os

data = data_manager.readData()
list_accounts = data_manager.getListAccounts(data)

## Обновить баланс в БД
def UpdateBalance():
    global data
    global list_accounts
    data = data_manager.setBalansInData(list_accounts, data)
    messageBalance(list_accounts, data, False)
    if os.path.isfile("ErrorAPI.txt"):
        ErrorMessage(data, "Проблемы с API")
    TimerUpdateBalance()

## Таймер. Кадый час запускает обновление баланса в БД
def TimerUpdateBalance():  
    timer_update_balance = threading.Timer(3600.0, UpdateBalance)
    timer_update_balance.start() 

## Рассылка сообщение. Если user_id имеет значение int не 0 то сообщение шлется конкретному ID аккаунту
def messageBalance(list_accounts, data_json, user_id):
    now_time = datetime.now() 
    for key in list_accounts:
        current_time = int(now_time.strftime("%H")) - data_json[key]["time_zone"]
        if (current_time == config.time_mailing) or (user_id):
            balance = data_json[key]["balance"]
            for id in data_json[key]["account_id"]:
                if (int(id) != user_id) and (user_id):
                    continue
                bot.send_message(id, f"Баланс аккаунта {key} {balance} руб.")

##Сообщение админу, если что то не так 
def ErrorMessage(data_json, messages):
    bot.send_message(data_json['admin']['account_id'], messages)
        


bot = telebot.TeleBot(config.token_bot)

UpdateBalance()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_id = types.KeyboardButton("Узнать мой ID")
    btn_balance = types.KeyboardButton("Узнать баланс")
    markup.add(btn_id, btn_balance)
    bot.send_message(message.chat.id, 'Хотите узнать свой ID', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def dialog(message):
    if (message.text == "Узнать мой ID"):
        user = message.from_user.id
        bot.send_message(message.chat.id, user)
        bot.send_message(message.chat.id, 'Это твой ID. Скопируй и отправь менеджеру.')
    elif(message.text=="Узнать баланс"):
        user = message.from_user.id
        messageBalance(list_accounts, data, user)
        bot.send_message(message.chat.id, 'Баланс обновляется 1 раз в час')
    else:
        bot.send_message(message.chat.id, 'Не знаю такой команды')

bot.polling(none_stop=True)
