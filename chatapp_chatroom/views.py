from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from chatapp_userprofile.models import User, Contacts

# Create your views here.

@login_required
def contact_query(request, my_id, friend_id):
    # The main purpose of this function is to query Contact table and return the query result 
    query = Contacts.objects.filter(
            (Q(user1=my_id.id) | Q(user1=friend_id.id)) & (Q(user2=friend_id.id) | Q(user2=my_id.id))
            )
    return query


@login_required
def chat_room(request):

    """ This function determine either two person are connected and they haven't blocked each other. 
    Freind request and block request is handled by the post method. Inside post method condition are checked which 
    button is pressed according to button name. If "friend_request" button is pressed then it create a contact object.
    If "block_user" button is pressed it check either user1 or user2 is the logged in user or not. Based on that it update
    the contact object value. If the status is "P" or "A" the block button will block the user else it will ublock the user.
    """
    
    try:
        friend_id = User.objects.get(id=request.GET.get('friend_id'))
    except:
        return render(request, 'utility/utility-404error.html')
    
    my_id = request.user
    
    if friend_id == my_id:   
        return redirect('user')
    
    contact_details = contact_query(request, my_id, friend_id)
    
    if request.method == "POST":
        if "friend_request" in request.POST:
            Contacts.objects.create(user1=my_id, user2=friend_id)
        elif "block_user" in request.POST:
            if contact_details[0].user1 == request.user:
                if contact_details[0].user1_status == 'P' or contact_details[0].user1_status == 'A':
                    contact_details.update(user1_status='B')
                else:
                    contact_details.update(user1_status='A')
            else:
                if contact_details[0].user2_status == 'P' or contact_details[0].user2_status == 'A':
                    contact_details.update(user2_status='B')
                else:
                    contact_details.update(user2_status='A')

            contact_details = contact_query(request, my_id, friend_id) # Get the updated query 
    
    context = {
        'friend_id': friend_id,
        'is_contact': contact_details.exists(),
        'contact_details': contact_details,
        'room_name': str(contact_details[0].room_id).replace("-", ""),
    }

    return render(request, 'chat/chat.html', context)



