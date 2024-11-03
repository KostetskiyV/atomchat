from django.urls import path

from .views import SenderAPIView, CreateChatAPIView, ReadChatAPIView

app_name = 'messenger'
urlpatterns = [
    path('send-message/', SenderAPIView.as_view()),
    path('create-chat/', CreateChatAPIView.as_view()),
    path('chat/<str:chatname>/', ReadChatAPIView.as_view())
]