from django.urls import path
from chatapp_dashboard import views

urlpatterns = [
    path('', views.dashboard, name='dashboard')
]
