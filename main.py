import telebot
from telebot import types
from chat import Chat, user_chats

TOKEN = '7978692660:AAHaIrRt7Zd60ZfXnSx7u2jgkn1Tq8yqGb0'
OPERATOR_CHAT_ID = '-4854428947'


myChat = Chat(TOKEN)
myChat.OPERATOR_CHAT_ID = OPERATOR_CHAT_ID

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(types.KeyboardButton('Каталог'), types.KeyboardButton('Чат'), types.KeyboardButton('FAQ'), types.KeyboardButton('Контакты'))

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back.add(types.KeyboardButton('Назад'))


@myChat.bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    user_chats[user_id] = {'status': 'menu'}
    myChat.bot.send_message(user_id, "Приветствуем в боте Phantom Prints!\n\n"
                                     "С помощью него Вы можете сделать онлайн заказ с автоматическим расчетом цены за фигурку вашего размера\n\n"
                                     "В разделе FAQ находятся ответы на часто задаваемые вопросы\n\n"
                                     "В чате вы можете написать по поводу персонального заказа или по иным вопросам\n\n"
                                     "В разделе контактов находятся ссылки на наши сообщества", reply_markup=menu)


@myChat.bot.message_handler(func=lambda m: m.text in ['Каталог', 'Чат', 'FAQ', 'Контакты', 'Назад'])
def text_messages(message):
    user_id = message.from_user.id
    if message.text == 'Каталог':
        myChat.bot.send_message(user_id, 'In progress')
    elif message.text == 'Чат':
        user_chats[user_id]['status'] = 'chat'
        myChat.bot.send_message(user_id, "Вы в чате с оператором. Напишите ваше сообщение. Для выхода из чата нажмите 'Назад'", reply_markup=back)
    elif message.text == 'FAQ':
        myChat.bot.send_message(user_id, "In progress", reply_markup=menu)
    elif message.text == 'Контакты':
        myChat.bot.send_message(user_id, "In progress", reply_markup=menu)
    elif message.text == 'Назад':
        user_chats[user_id]['status'] = 'menu'
        myChat.bot.send_message(user_id, "Вы в меню, чем Вам помочь?", reply_markup=menu)


if __name__ == '__main__':
    myChat.start_work()
    myChat.run()