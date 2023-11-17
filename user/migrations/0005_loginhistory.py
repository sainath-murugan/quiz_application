# Generated by Django 4.2.4 on 2023-11-10 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_customuser_authenticator_enable'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('browser', models.CharField(max_length=255)),
                ('device', models.CharField(max_length=255)),
                ('bot', models.BooleanField(default=False, help_text='marked as verified, if it is bot')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]