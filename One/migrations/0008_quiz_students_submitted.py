# Generated by Django 4.2.4 on 2023-11-08 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('One', '0007_remove_quiz_students_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='students_submitted',
            field=models.ManyToManyField(blank=True, related_name='students_submitted_quiz', to='One.userprofilestudent'),
        ),
    ]