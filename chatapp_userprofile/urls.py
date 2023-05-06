from django.urls import path
from chatapp_userprofile import views

urlpatterns = [
    path('', views.user_profile, name='user')
]
