# Generated by Django 5.1.1 on 2024-12-09 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iam', '0007_alter_auditreport_audit_id_and_more'),
        ('main_app', '0007_group_alter_staff_department_staff_group_section_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followup',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.staff'),
        ),
    ]
