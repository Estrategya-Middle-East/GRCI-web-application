# Generated by Django 5.1.1 on 2024-11-16 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_department_descripton'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='descripton',
            new_name='description',
        ),
    ]
