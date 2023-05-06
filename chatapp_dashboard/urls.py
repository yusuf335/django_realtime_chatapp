from django.urls import path
from chatapp_dashboard import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search-user/', views.search_user, name='search_user')
]
