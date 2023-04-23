"""chatapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from chatapp import views
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Login View
    path('', views.login_view, name='login'),

    # Logout View
    path('logout/', views.logout_view, name='logout'),

    # Signup View
    path('signup/', views.signup, name='signup'),

    # Account activation
    path('activate/<uidb64>/<token>/',views.activate, name='activate'), 

    # Dashboards View
    path('dashboard/',include('chatapp_dashboard.urls'), name='dashboard'), 
]

