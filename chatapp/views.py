from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpRequest

from .forms import LoginForm, RegistrationForm ,ResetPasswordForm
from chatapp_userprofile.models import User

UserModel = get_user_model()

# Error Message on login Page
def show_error(request, message):
    resend_email = None
    login_form = LoginForm()

    if message == "not_verified":
        message = f"Your account is not verified! Please check spam folder for the activation email or click the button below to receive the activation link at {request.POST.get('email')}" 
        resend_email = True
        
    context = {
        'resend_email': resend_email,
        'message': message,
        'login_form': login_form,
    }

    return render(request,"authentication/login.html",context)
    # return render(request,"email/confirmation_link.html",context)

#Login 
def login_view(request):
# Chek if user is authenticated or not 
    if request.user.is_authenticated:
    # If authenticated then redirect to dashboard
        return redirect('dashboard')
    else:
        # Check is the request method is POST
        if 'login' in request.POST:
            # Try to get the user submitted in the login form
            try:
                user_info = User.objects.get(email=request.POST.get('email'))
            except ObjectDoesNotExist:
                return show_error(request, message="Incorrect email or password!")
            
            form = LoginForm(request.POST, instance=user_info)
            if form.is_valid():
                email=request.POST.get('email')
                password=request.POST.get('password')

                # Official Documentation is followed
                # https://docs.djangoproject.com/en/4.0/topics/auth/

                user = authenticate(request, email=email, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    if user_info != True:
                        return show_error(request, message="not_verified")
                    else:
                        return show_error(request, message="Incorrect email or password!")
            else:
                return show_error(request, message="Please check the reCaptcha box!")
        elif 'email_resend' in request.POST:
            try:
                user_info = User.objects.get(email=request.POST.get('email'))
            except ObjectDoesNotExist:
                return show_error(request, message="Incorrect email or password!")

            try:
                mail_subject = 'Activate your account.'
                message = render_to_string('email/confirmation_link.html', {
                    'user': user_info,
                    'domain': HttpRequest.get_host(request),
                    'uid': urlsafe_base64_encode(force_bytes(user_info.pk)),
                    'token': default_token_generator.make_token(user_info),
                })
                to_email = user_info.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.content_subtype = 'html'
                email.send()
                return show_error(request, message=None)
            except:
                return show_error(request, message="Failed to send email please try again or contact the adim")
        else:
            return show_error(request, message=None)


#Signup
def signup(request):

    message = None
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save(commit=False)
            user.is_active = False
            user.save()
            mail_subject = 'Activate your account.'
            message = render_to_string('email/confirmation_link.html', {
                'user': user,
                'domain': HttpRequest.get_host(request),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = registration_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
            return redirect('login')
    else:
        registration_form = RegistrationForm()
    message = registration_form.errors

    context = {
        'message': message,
        'registration_form': registration_form,
    }
    return render(request, 'authentication/signup.html', context)



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        context = {}
        return render(request,"authentication/logout-success.html", context)
    else:
        return redirect('login')
    

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'authentication/account_activated.html')
    else:
        return render(request, 'authentication/invalid_activation_link.html')