# Generated by Django 5.1.1 on 2024-12-27 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erm', '0036_alter_riskass_risk_heatmap_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskdefine',
            name='risk_cause',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='riskdefine',
            name='risk_event',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='riskdefine',
            name='risk_impact',
            field=models.TextField(blank=True, null=True),
        ),
    ]
