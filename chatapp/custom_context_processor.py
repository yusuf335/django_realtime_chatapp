import datetime
from django.db.models import Q

def user_context(request):

   try:
      return {
         'user': request.user,
    }

   except Exception as e:

      return {
    }
    