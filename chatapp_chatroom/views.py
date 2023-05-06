from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from chatapp_userprofile.models import User, Contacts

# Create your views here.

@login_required
def chat_room(request):
    user_id = request.GET.get('user_id')
    try:
        user= User.objects.get(id=user_id)
    except:
        return render(request, 'utility/utility-404error.html')
    
    my_id = request.user.id

    is_contact = Contacts.objects.filter(
                (Q(user1=user_id) and Q(user2=my_id)) 
                or 
                (Q(user1=my_id) and Q(user2=user_id))
                )
    
    is_contact = is_contact.exists()

    context = {
        'user': user,
        'is_contact': is_contact,
        'contact_details': is_contact,
    }
    return render(request, 'chat/chat.html', context)



