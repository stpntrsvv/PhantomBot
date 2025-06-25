from telebot import types
from chat import Chat, user_chats

TOKEN = '7978692660:AAHaIrRt7Zd60ZfXnSx7u2jgkn1Tq8yqGb0'
OPERATOR_CHAT_ID = '-4854428947'

myChat = Chat(TOKEN)
myChat.OPERATOR_CHAT_ID = OPERATOR_CHAT_ID

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
back = types.ReplyKeyboardMarkup(resize_keyboard=True)
categories = types.ReplyKeyboardMarkup(resize_keyboard=True)
waha_figs = types.ReplyKeyboardMarkup(resize_keyboard=True)
product = types.ReplyKeyboardMarkup(resize_keyboard=True)

menu.add(types.KeyboardButton('Каталог'), types.KeyboardButton('Чат'), types.KeyboardButton('FAQ'), types.KeyboardButton('Контакты'))
back.add(types.KeyboardButton('В меню'))
categories.add(types.KeyboardButton('Warhammer'))
waha_figs.add(types.KeyboardButton('Demon Warrior'), types.KeyboardButton('Redemptor Dreadnought'))
product.add(types.KeyboardButton('Заказать'), types.KeyboardButton('Изменить размер'), types.KeyboardButton('В меню'))

catalogue_buttons = ['Warhammer', 'Demon Warrior', 'Redemptor Dreadnought', 'Заказать', 'Изменить размер', 'В меню']


@myChat.bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    user_chats[user_id] = {'status': 'menu', 'curr_id': 0}
    myChat.bot.send_message(user_id, "Приветствуем в боте Phantom Prints!\n\n"
                                     "С помощью него Вы можете сделать онлайн заказ с автоматическим расчетом цены за фигурку вашего размера\n\n"
                                     "В разделе FAQ находятся ответы на часто задаваемые вопросы\n\n"
                                     "В чате вы можете написать по поводу персонального заказа или по иным вопросам\n\n"
                                     "В разделе контактов находятся ссылки на наши сообщества", reply_markup=menu)


@myChat.bot.message_handler(func=lambda m: m.text in ['Каталог', 'Чат', 'FAQ', 'Контакты', 'В меню'])
def text_messages(message):
    user_id = message.from_user.id
    if message.text == 'Каталог':
        myChat.bot.send_message(user_id, 'Добро пожаловать в каталог! Выберите категорию и фигурку:',
                                reply_markup=categories)
    elif message.text == 'Чат':
        user_chats[user_id]['status'] = 'chat'
        myChat.bot.send_message(user_id,
                                "Вы в чате с оператором. Напишите ваше сообщение. Для выхода из чата нажмите 'Назад'",
                                reply_markup=back)
    elif message.text == 'FAQ':
        myChat.bot.send_message(user_id, "In progress", reply_markup=menu)
    elif message.text == 'Контакты':
        myChat.bot.send_message(user_id, "In progress", reply_markup=menu)
    elif message.text == 'В меню':
        user_chats[user_id]['status'] = 'menu'
        myChat.bot.send_message(user_id, "Вы в меню, чем Вам помочь?", reply_markup=menu)


@myChat.bot.message_handler(func=lambda m: m.text in catalogue_buttons)
def catalogue_messages(message):
    user_id = message.from_user.id
    if message.text == 'Warhammer':
        myChat.bot.send_message(user_id, "Раздел: 'Warhammer'", reply_markup=waha_figs)
    elif message.text == 'Demon Warrior':
        user_chats[user_id]['curr_id'] = 1
        myChat.bot.send_photo(user_id, 'https://i.imgur.com/HIfFZm7.jpeg')
        myChat.bot.send_message(user_id, 'Demon Warrior\nВысота: 10 см\nЦена: 1500 руб.\n'
                                         'Будьте внимательны! Цена считается без учета покраски', reply_markup=product)
    elif message.text == 'Redemptor Dreadnought':
        user_chats[user_id]['curr_id'] = 2
        myChat.bot.send_photo(user_id, 'example_stlfiles/2/PrimeDread.jpg')
        myChat.bot.send_message(user_id, reply_markup=back)
    elif message.text == 'Заказать':
        user_chats[user_id]['status'] = 'order'
        curr_id = user_chats[user_id].get('curr_id', 0)
        order_msg = myChat.bot.send_message(
            OPERATOR_CHAT_ID,
            f"Новый заказ от пользователя {user_id}:\nМодель: {curr_id}\n"
            f"Ответьте на это сообщение текстом 'подтверждено', чтобы подтвердить заказ.")
        user_chats[user_id]['order_msg_id'] = order_msg.message_id
        myChat.bot.send_message(
            user_id,
            'Ваш заказ отправлен оператору! Ожидайте подтверждения.',
            reply_markup=back
        )
    elif message.text == 'В меню':
        user_chats[user_id]['status'] = 'menu'
        myChat.bot.send_message(user_id, "Вы в меню, чем Вам помочь?", reply_markup=menu)


if __name__ == '__main__':
    myChat.start_work()
    myChat.run()
