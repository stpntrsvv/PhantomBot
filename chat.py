import telebot
from telebot import types

user_chats = {}  # user_chats: {user_id: {'status': 'active', 'operator_msg_id': msg_id, 'order_msg_id': msg_id}}


class Chat:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.OPERATOR_CHAT_ID = None

    def run(self):
        self.bot.infinity_polling()

    def start_work(self):
        @self.bot.message_handler(func=lambda message: str(message.chat.id) != self.OPERATOR_CHAT_ID)
        def handle_user_message(message):
            user_id = message.from_user.id
            if user_id not in user_chats or user_chats[user_id]['status'] not in ['chat', 'order']:
                return

            if user_chats[user_id]['status'] == 'chat':
                forwarded = self.bot.forward_message(self.OPERATOR_CHAT_ID, user_id, message.message_id)
                user_chats[user_id]['operator_msg_id'] = forwarded.message_id
                self.bot.send_message(user_id, "Ваше сообщение передано оператору. Ожидайте ответа.")

        @self.bot.message_handler(func=lambda message: str(message.chat.id) == self.OPERATOR_CHAT_ID and message.reply_to_message)
        def handle_operator_reply(message):
            for user_id, data in user_chats.items():
                if 'order_msg_id' in data and data['order_msg_id'] == message.reply_to_message.message_id:
                    if message.text.lower() == 'подтверждено':
                        self.bot.send_message(
                            user_id,
                            "✅ Ваш заказ подтвержден оператором! Скоро с вами свяжутся."
                        )
                        self.bot.send_message(
                            self.OPERATOR_CHAT_ID,
                            f"Заказ пользователя {user_id} подтвержден."
                        )
                    else:
                        self.bot.send_message(
                            self.OPERATOR_CHAT_ID,
                            "Чтобы подтвердить заказ, ответьте 'подтверждено' на сообщение с заказом."
                        )
                    return

            original_msg = message.reply_to_message
            for uid, data in user_chats.items():
                if 'operator_msg_id' in data and data['operator_msg_id'] == original_msg.message_id:
                    self.bot.send_message(uid, f"{message.text}")
                    return

            self.bot.send_message(self.OPERATOR_CHAT_ID, "Не удалось найти пользователя для ответа.")

        # Обработчик прямых сообщений оператора (не ответов)
        @self.bot.message_handler(
            func=lambda message: str(message.chat.id) == self.OPERATOR_CHAT_ID and not message.reply_to_message)
        def handle_operator_direct_message(message):
            self.bot.send_message(self.OPERATOR_CHAT_ID, "Отвечайте на конкретные сообщения пользователей.")