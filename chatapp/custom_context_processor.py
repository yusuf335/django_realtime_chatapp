from django.db.models import Q

# This template context processor help to pass data to sidebar or any place user data is needed

def user_context(request):

   try:
      return {
         'sidebar_user_details': request.user,
    }

   except Exception as e:

      return {
    }
    