from django.db import models
from rest_framework import serializers

from authapp.models import User

class ChatManager(models.Manager):
    def create_chat(self, chatname, usernames, creator_id):

        if chatname is None:
            raise TypeError('Chat must hava a name.')

        for username in usernames:
            if username is None:
                raise TypeError('User must be named.')

            if not (User.objects.filter(username=username) & User.objects.filter(is_active=True)).exists():
                raise serializers.ValidationError('User with specified username does`t exist or blocked.')

        chat = self.model(name = chatname)
        chat.save()
        users = User.objects.filter(username__in = usernames) | User.objects.filter(id = creator_id)
        chat.users.set(users, through_defaults = {})
        chat.save()
        return {'name': chat, 'users': chat.get_users()}

    def get_messages(self, chatname, user_id):

        if not Chat.objects.filter(name = chatname).exists():
            raise serializers.ValidationError("Specified chat does`t exist.")

        if not (User.objects.filter(id = user_id) & User.objects.filter(is_active=True)).exists():
            raise serializers.ValidationError('User with specified username does`t exist or blocked.')

        if not (Chat.objects.filter(name = chatname) & Chat.objects.filter(users__id = user_id)).exists():
            if not User.objects.get(id = user_id).is_staff:
                raise serializers.ValidationError('User with specified username is`t in chat.')

        messages = (Message.objects.filter(chat__name = chatname) & Message.objects.filter(user__is_active = True)).order_by('wrote_at').values('user_id', 'wrote_at', 'text')
        messages_list = []
        for message in messages:
            datetime = message['wrote_at'].strftime("%d/%m/%Y, %H:%M:%S")
            username = User.objects.get(id = message['user_id'])
            text = message['text']
            messages_list.append({'datetime': datetime, 'username': username, 'text': text})
        return messages_list

class Chat(models.Model):
    name = models.CharField(max_length = 40, unique = True)

    users = models.ManyToManyField(User, through='ChatUsers')

    objects = ChatManager()

    def __str__(self):
        return self.name

    def get_users(self):
        return self.users.all()

class ChatUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

class MessageManager(models.Manager):
    def create_message(self, text, chatname, user_id):
        if text is None:
            raise TypeError('Message text can`t be empty.')

        if chatname is None:
            raise TypeError('An chatname is required to send message.')

        if not (User.objects.filter(id=user_id) & User.objects.filter(is_active=True)).exists():
            raise serializers.ValidationError('User with specified username does`t exist or blocked.')

        if not Chat.objects.filter(name=chatname).exists():
            raise serializers.ValidationError('Chat with specified name does`t exist.')

        if not (Chat.objects.filter(name = chatname) & Chat.objects.filter(users__id = user_id)).exists():
            raise serializers.ValidationError('User with specified name is`t in chat.')

        message = self.model(text = text)
        message.user_id = user_id
        message.chat = Chat.objects.get(name = chatname)
        message.save()
        username = User.objects.get(id = user_id)
        return {'username': username, 'wrote_at': message.get_time().strftime("%d/%m/%Y, %H:%M:%S"), 'chatname': chatname, 'text': message.text}

class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    chat = models.ForeignKey(Chat, on_delete = models.CASCADE)

    text = models.CharField(max_length=1500)

    wrote_at = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

    def __str__(self):
        return self.text

    def get_time(self):
        return self.wrote_at