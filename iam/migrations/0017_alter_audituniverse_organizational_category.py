# Generated by Django 5.1.1 on 2025-01-08 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iam', '0016_audituniverse_audit_scope_audituniverse_entity_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audituniverse',
            name='organizational_category',
            field=models.CharField(choices=[('Department', 'Department'), ('Division', 'Division'), ('Business Unit', 'Business Unit')], default='Department', max_length=50),
        ),
    ]
