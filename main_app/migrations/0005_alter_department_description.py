# Generated by Django 5.1.1 on 2024-11-16 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_rename_descripton_department_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
