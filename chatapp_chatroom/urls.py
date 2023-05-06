from django.urls import path
from chatapp_chatroom import views

urlpatterns = [
    path('', views.chat_room, name="chatroom")
]
