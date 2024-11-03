from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import LoginSerializer, RegistrationSerializer, BlockSerializer, UserDataSerializer


class RegistrationAPIView(APIView):

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class BlockAPIView(APIView):

    permission_classes = (IsAdminUser,)
    serializer_class = BlockSerializer

    def post(self, request):
        users = request.data.get('users', {})

        serializer = self.serializer_class(data=users, context={"block": True})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class UnlockAPIView(APIView):

    permission_classes = (IsAdminUser,)
    serializer_class = BlockSerializer

    def post(self, request):
        users = request.data.get('users', {})

        serializer = self.serializer_class(data=users, context={"block": False})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDataAPIView(APIView):

    permission_classes = (IsAdminUser,)
    serializer_class = UserDataSerializer

    def get(self, request, username):

        serializer = self.serializer_class(data={}, context={"username": username})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)