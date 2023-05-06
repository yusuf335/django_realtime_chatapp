import datetime
from django.db.models import Q

def user_context(request):

   try:
      return {
         'sidebar_user_details': request.user,
    }

   except Exception as e:

      return {
    }
    