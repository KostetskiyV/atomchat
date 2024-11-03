import jwt

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import SenderJSONRenderer, CreateChatJSONRenderer
from .serializers import SenderSerializer, CreateChatSerializer, ReadChatSerializer
from atomsite import settings

class SenderAPIView(APIView):

    permission_classes = (IsAuthenticated,)
    renderer_classes = (SenderJSONRenderer,)
    serializer_class = SenderSerializer

    def post(self, request):
        user_token = request.headers['Token']
        user_id = jwt.decode(user_token, settings.SECRET_KEY, algorithms='HS256')['id']
        message = request.data.get('message', {})

        serializer = self.serializer_class(data=message, context={"user_id": user_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CreateChatAPIView(APIView):

    permission_classes = (IsAuthenticated,)
    renderer_classes = (CreateChatJSONRenderer,)
    serializer_class = CreateChatSerializer

    def post(self, request):
        user_token = request.headers['Token']
        user_id = jwt.decode(user_token, settings.SECRET_KEY, algorithms='HS256')['id']
        chat = request.data.get('chat', {})

        serializer = self.serializer_class(data=chat, context={"creator_id": user_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReadChatAPIView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ReadChatSerializer

    def get(self, request, chatname):
        user_token = request.headers['Token']
        user_id = jwt.decode(user_token, settings.SECRET_KEY, algorithms='HS256')['id']

        serializer = self.serializer_class(data={}, context={"chatname": chatname, "user_id": user_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)