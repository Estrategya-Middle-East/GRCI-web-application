# Generated by Django 5.1.1 on 2024-12-28 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erm', '0040_alter_risk_workflow_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='risk',
            old_name='Residual_approval_status',
            new_name='residual_approval_status',
        ),
    ]
