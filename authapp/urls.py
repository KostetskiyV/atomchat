from django.urls import path

from .views import *

app_name = 'authentication'
urlpatterns = [
    path('registrate/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('block/', BlockAPIView.as_view()),
    path('unlock/', UnlockAPIView.as_view()),
    path('user/<str:username>/', UserDataAPIView.as_view())
]