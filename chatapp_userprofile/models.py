import os
import uuid
from django.db import models
from django.utils.translation import gettext_lazy
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from hashid_field import HashidAutoField

from django.core.exceptions import ValidationError


def validate_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

# Const value used in the model
user_profile = 'user_profile/%Y/%m/'




class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class STATUS(models.TextChoices):
        NEW = 'N', 'New entry'
        ACTIVE = 'A', 'Active'
        RESTRCITED = 'U', 'Restricted'

    id = HashidAutoField(primary_key=True)
    email = models.EmailField(gettext_lazy('email_address'), unique=True)
    name = models.CharField(max_length=150)
    status = models.CharField(choices=STATUS.choices, max_length=1, default=STATUS.ACTIVE)
    status_updated = models.DateTimeField(auto_now_add=True, null=True)
    image = models.FileField(upload_to=user_profile, blank=True, validators=[validate_extension ], null=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.name
    

class Contacts(models.Model):
    class STATUS(models.TextChoices):
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        BLOCKED = 'B', 'Blocked'
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact')
    room_id = models.UUIDField(default=uuid.uuid4, editable=False)
    user1_status = models.CharField(choices=STATUS.choices, max_length=1, default=STATUS.PENDING)
    user2_status = models.CharField(choices=STATUS.choices, max_length=1, default=STATUS.PENDING)

    class Meta:
        db_table = 'user_contacts'

