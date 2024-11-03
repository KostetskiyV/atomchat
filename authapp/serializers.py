from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError('An username is required to log in.')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this username and password was not found.')
        
        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {
            'username': user.username,
            'token': user.token
        }

class BlockSerializer(serializers.ModelSerializer):

    usernames = serializers.ListField(child=serializers.CharField(max_length = 25))

    class Meta:
        model = User
        fields = ['usernames']

    def create(self, validated_data):
        if self.context.get('block'):
            return User.objects.block_users(**validated_data)
        else:
            return User.objects.unlock_users(**validated_data)

class UserDataSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=25, read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'token']

    def create(self, data):
        return User.objects.get_by_natural_key(self.context.get('username'))
