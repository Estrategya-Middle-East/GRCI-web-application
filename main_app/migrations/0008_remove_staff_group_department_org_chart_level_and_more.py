# Generated by Django 5.1.1 on 2024-12-28 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_group_alter_staff_department_staff_group_section_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='group',
        ),
        migrations.AddField(
            model_name='department',
            name='org_chart_level',
            field=models.CharField(blank=True, choices=[('N1', 'N1'), ('N2', 'N2'), ('N3', 'N3'), ('N4', 'N4')], default=None, max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='Group',
        ),
    ]
