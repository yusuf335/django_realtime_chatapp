from django import forms
from django.contrib.auth.forms import UserCreationForm
from chatapp_userprofile.models import User
from captcha.fields import ReCaptchaField

# login form with captcha feild
class LoginForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control', 'type': 'email', 'required': 'True'}),
            'password': forms.TextInput(attrs={'class':'form-control', 'type': 'password','required': 'True'}),
        }

# Registration Form
class RegistrationForm(UserCreationForm):
    captcha = ReCaptchaField()
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password','required': 'True'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password','required': 'True'}))
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'type': 'text','required': 'True'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'type': 'email', 'required': 'True'}),
        }


# Reset password form
class ResetPasswordForm(forms.Form):
    captcha = ReCaptchaField()
    email = forms.CharField( widget = forms.TextInput(attrs={'class':'form-control', 'type': 'email'}))