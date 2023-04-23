from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


# Dashboard
@login_required
def dashboard(request):
    greeting = {}       
    return render(request, 'dashboard/dashboard.html',greeting)