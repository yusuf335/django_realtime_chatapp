# Generated by Django 4.2 on 2023-05-16 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp_userprofile', '0004_rename_status_contacts_user1_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='image',
        ),
    ]