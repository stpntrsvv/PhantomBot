from telebot import types
from chat import Chat, user_chats
from stl_script import stl_script

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
waha_figs.add(types.KeyboardButton('Demon Warrior'), types.KeyboardButton('Redemptor Dreadnought'), types.KeyboardButton('В меню'))
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
        myChat.bot.send_message(user_id, 'Добро пожаловать в каталог! Выберите категорию и фигурку:', reply_markup=categories)
    elif message.text == 'Чат':
        user_chats[user_id]['status'] = 'chat'
        myChat.bot.send_message(user_id, "Вы в чате с оператором. Напишите ваше сообщение. Для выхода из чата нажмите 'В меню'", reply_markup=back)
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
        myChat.bot.send_photo(user_id, 'https://i.ibb.co/rGCnntpJ/g-Uv-URr-Ab8-N6u-Zr-Ej9hrs8umc-Bua6q-JYJYa-Wq-Iffg2ovf-TULGEU3-S2wu-O5-BPq-X-0sn6v-Lk-2-WGjg5-MR1-UD.jpg')
        myChat.bot.send_message(user_id, 'Demon Warrior\nВысота: 5 см\nЦена: 1700 руб.\n'
                                     'Будьте внимательны! Цена считается без учета покраски', reply_markup=product)
    elif message.text == 'Redemptor Dreadnought':
        user_chats[user_id]['curr_id'] = 2
        myChat.bot.send_photo(user_id, 'https://i.ibb.co/SDWzmxZR/o48-Gst-EBTGxdvx-N8uap-Udy-D3-FXSg-Cx7z3s6-Audl-IAFedw-Ggrj-S6-Kmr-Hgl-IDin-TTZ397-I3-wx-JZN4-Ev8h-Y.jpg')
        myChat.bot.send_message(user_id, 'Redemptor Dreadnought\nВысота: 10 см\nЦена: 4000 руб.\n'
                                         'Будьте внимательны! Цена считается без учета покраски', reply_markup=product)
    elif message.text == 'Заказать':
        user_chats[user_id]['status'] = 'order'
        curr_id = user_chats[user_id].get('curr_id', 0)
        # Получаем текущий размер и цену (если они были изменены)
        new_size = user_chats[user_id].get('new_size', None)
        new_price = user_chats[user_id].get('new_price', None)

        order_text = f"Новый заказ от пользователя {user_id}:\nМодель: {curr_id}\n"
        if new_size is not None and new_price is not None:
            order_text += f"Новый размер: {new_size} мм\nНовая цена: {new_price} руб.\n"

        order_msg = myChat.bot.send_message(
            OPERATOR_CHAT_ID,
            order_text + "\nОтветьте на это сообщение текстом 'подтверждено', чтобы подтвердить заказ.")

        user_chats[user_id]['order_msg_id'] = order_msg.message_id
        myChat.bot.send_message(user_id, 'Ваш заказ отправлен оператору! Ожидайте подтверждения.', reply_markup=back)
    elif message.text == 'Изменить размер':
        myChat.bot.send_message(user_id, "Введите высоту фигурки в мм (только число):", reply_markup=types.ForceReply(selective=True))
        user_chats[user_id]['awaiting_size'] = True

    elif message.text == 'В меню':
        user_chats[user_id]['status'] = 'menu'
        myChat.bot.send_message(user_id, "Вы в меню, чем Вам помочь?", reply_markup=menu)


@myChat.bot.message_handler(func=lambda m: user_chats.get(m.from_user.id, {}).get('awaiting_size'))
def handle_size_input(message):
    user_id = message.from_user.id
    user_data = user_chats[user_id]

    myChat.bot.send_message(user_id, 'Пожалуйста, подождите')

    if message.text.replace('.', '', 1).isdigit():
        new_size = float(message.text)
        curr_id = user_data.get('curr_id', 0)
        new_price = int(stl_script(curr_id, new_size))

        # Сохраняем новый размер и цену
        user_data['new_size'] = new_size
        user_data['new_price'] = new_price

        myChat.bot.send_message(user_id, f"Теперь цена вашей фигурки - {new_price} руб.", reply_markup=product)

        del user_data['awaiting_size']
    else:
        myChat.bot.send_message(user_id, "Пожалуйста, введите число (например: 10.5)")


if __name__ == '__main__':
    myChat.start_work()
    myChat.run()
