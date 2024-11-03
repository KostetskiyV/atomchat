from django.test import TestCase

from messageapp import models as message_models
from authapp import models as auth_models

class ModelTest(TestCase):
    def test_chat_model_create_chat(self):
        creator = auth_models.User.objects.create_user("creator").id
        usernames = [f"user{i}" for i in range(1000)]
        for i in usernames:
            auth_models.User.objects.create_user(i)

        message_models.Chat.objects.create_chat("chat1", usernames, creator)
        created_chat_users = message_models.Chat.objects.latest("id").users.values_list("username", flat=True)
        self.assertEqual(list(created_chat_users), ["creator"] + usernames)

        creator = auth_models.User.objects.get(username = usernames[0]).id
        message_models.Chat.objects.create_chat("chat2", usernames, creator)
        created_chat_users = message_models.Chat.objects.latest("id").users.values_list("username", flat=True)
        self.assertEqual(list(created_chat_users), usernames)

    def test_chat_model_create_message(self):
        user_id = auth_models.User.objects.create_user("user").id
        message_models.Chat.objects.create_chat("chat", ["user"], user_id)
        for i in range(1, 1501):
            message = message_models.Message.objects.create_message('a'*i, 'chat', user_id)
            created_message = message_models.Message.objects.latest("id")
            self.assertEqual(message, {"username": created_message.user, "wrote_at": created_message.wrote_at.strftime("%d/%m/%Y, %H:%M:%S"), "chatname": created_message.chat.name, "text": created_message.text})

    def test_chat_model_get_messages(self):
        user_id = auth_models.User.objects.create_user("user").id
        message_models.Chat.objects.create_chat("chat", ["user"], user_id)
        messages = []
        for i in range(1, 1501):
            message = message_models.Message.objects.create_message('a'*i, 'chat', user_id)
            messages.append({'datetime': message["wrote_at"], 'username': message["username"], 'text': message["text"]})
        readed_messages = message_models.Chat.objects.get_messages('chat', user_id)
        self.assertEqual(messages, readed_messages)