from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from chatapp_userprofile.models import User, Contacts

# Create your views here.


@login_required
def user_profile(request):

    return render(request, 'profile/profile.html')



