import telebot
from telebot import types

user_chats = {}     # user_chats: {user_id: {'status': 'active', 'operator_msg_id': msg_id}}

class Chat:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        pass

    def run(self):
        self.bot.infinity_polling()

    def start_work(self):
        @self.bot.message_handler(func=lambda message: str(message.chat.id) != self.OPERATOR_CHAT_ID)
        def handle_user_message(message):
            user_id = message.from_user.id
            if user_id not in user_chats or user_chats[user_id]['status'] != 'chat':
                return
            forwarded = self.bot.forward_message(self.OPERATOR_CHAT_ID, user_id, message.message_id)
            user_chats[user_id]['operator_msg_id'] = forwarded.message_id
            self.bot.send_message(user_id, "Ваше сообщение передано оператору. Ожидайте ответа.")

        @self.bot.message_handler(func=lambda message: str(message.chat.id) == self.OPERATOR_CHAT_ID)
        def handle_operator_message(message):
            if message.reply_to_message:
                original_msg = message.reply_to_message
                user_id = None
                for uid, data in user_chats.items():
                    if 'operator_msg_id' in data and data['operator_msg_id'] == original_msg.message_id:
                        user_id = uid
                        break

                if user_id:
                    self.bot.send_message(user_id, f"{message.text}")
                else:
                    self.bot.send_message(self.OPERATOR_CHAT_ID, "Не удалось найти пользователя для ответа.")