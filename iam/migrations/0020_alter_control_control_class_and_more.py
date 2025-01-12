# Generated by Django 5.1.1 on 2025-01-12 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iam', '0019_remove_control_process_id_control_subprocess_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='control_class',
            field=models.CharField(blank=True, choices=[('Operational', 'Operational'), ('Strategic', 'Strategic'), ('Financial', 'Financial'), ('Compliance', 'Compliance')], default='Operational', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='control',
            name='control_type',
            field=models.CharField(blank=True, choices=[('Preventive', 'Preventive'), ('Detective', 'Detective'), ('Concurrent', 'Concurrent')], default='Preventive', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='processrisk',
            name='risk_type',
            field=models.CharField(blank=True, choices=[('Operational', 'Operational'), ('Strategic', 'Strategic'), ('Financial', 'Financial'), ('Compliance', 'Compliance')], default='Operational', max_length=50, null=True),
        ),
    ]
