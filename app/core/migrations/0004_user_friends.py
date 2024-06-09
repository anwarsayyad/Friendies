# Generated by Django 5.0 on 2024-06-08 18:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_friends_req_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, through='core.Friends', to=settings.AUTH_USER_MODEL),
        ),
    ]