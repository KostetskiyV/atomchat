from rest_framework import serializers

from .models import Message, Chat


class SenderSerializer(serializers.ModelSerializer):

    text = serializers.CharField(max_length=1500)
    username = serializers.CharField(max_length=25, read_only=True)
    chatname = serializers.CharField(max_length=40)
    wrote_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ['text', 'wrote_at', 'username', 'chatname']


    def create(self, validated_data):
        user_id = self.context.get('user_id')
        return Message.objects.create_message(**validated_data, user_id=user_id)

class CreateChatSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=40)
    users = serializers.ListField(child=serializers.CharField(max_length = 25))

    class Meta:
        model = Chat
        fields = ['name', 'users']

    def create(self, validated_data):
        chatname = validated_data.get('name', None)
        usernames = validated_data.get('users', None)
        creator_id = self.context.get('creator_id')

        return Chat.objects.create_chat(chatname, usernames, creator_id)

class MessageSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    username = serializers.CharField(max_length=25)
    text = serializers.CharField(max_length=1500)

class ReadChatSerializer(serializers.Serializer):

    messages = serializers.ListSerializer(child=MessageSerializer(), read_only=True)

    def create(self, data):
        chatname = self.context.get("chatname")
        user_id = self.context.get("user_id")

        return {'messages': Chat.objects.get_messages(chatname, user_id)}