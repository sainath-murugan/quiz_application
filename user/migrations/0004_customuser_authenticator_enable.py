# Generated by Django 4.2.4 on 2023-11-10 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_customuser_authenticator'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='authenticator_enable',
            field=models.BooleanField(default=False, help_text='marked as verified, if 2FA is enabled'),
        ),
    ]
