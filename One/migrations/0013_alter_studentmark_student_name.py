# Generated by Django 4.2.4 on 2023-11-08 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('One', '0012_quiz_students_submitted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmark',
            name='student_name',
            field=models.EmailField(max_length=254),
        ),
    ]
