# Generated by Django 5.1.1 on 2024-11-29 18:28

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erm', '0012_rename_risk_type_riskdefine_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskPrioritization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('risk_score', models.IntegerField(default=0)),
                ('priority_level', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Critical', 'Critical')], default='Medium', max_length=50)),
                ('justification', models.CharField(blank=True, max_length=255, null=True)),
                ('assessed_to', models.CharField(blank=True, max_length=255, null=True)),
                ('next_reviewdate', models.DateField(default=django.utils.timezone.now)),
                ('review_frequency', models.CharField(choices=[('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Annually', 'Annually')], default='Monthly', max_length=50)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Closed', 'Closed')], default='Open', max_length=50)),
                ('comments', models.TextField(null=True)),
                ('is_manual_edit', models.BooleanField(default=False)),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('under_review', 'Under Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=50)),
                ('risk', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='prioritization_step', to='erm.risk')),
            ],
        ),
    ]
