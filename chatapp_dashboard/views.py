from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from chatapp_userprofile.models import User




# Create your views here.

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def search_user(request):
    if is_ajax(request=request):
        user_id = request.POST.get('user_id').replace(" ", "")
        err = {
                    'message': 'No User Found!',
                }
        
        if len(user_id) >= 6:
            try:
                query_search = User.objects.get(id=user_id)
                
                item = {
                    'id': query_search.id,
                    'name': query_search.name,
                }

                res = item
            except:
                res = err
        else:
            res = err
            
        return JsonResponse({'data':res})
    
    return JsonResponse({})

# Dashboard
@login_required
def dashboard(request):
    
    greeting = {
    }       
    return render(request, 'dashboard/dashboard.html',greeting)