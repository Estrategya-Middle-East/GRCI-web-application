# Generated by Django 5.1.1 on 2024-11-29 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erm', '0005_remove_objective_department_and_more'),
        ('main_app', '0007_group_alter_staff_department_staff_group_section_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objective',
            name='kpis_linked',
            field=models.ManyToManyField(to='erm.kpi'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='owner',
            field=models.ManyToManyField(to='main_app.staff'),
        ),
    ]
