# Generated by Django 5.1.1 on 2024-12-08 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iam', '0006_alter_audituniverseregister_risk_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditreport',
            name='audit_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iam.audituniverseregister'),
        ),
        migrations.AlterField(
            model_name='documentmanagement',
            name='audit_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iam.audituniverseregister'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='audit_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iam.audituniverseregister'),
        ),
        migrations.AlterField(
            model_name='qualityassurance',
            name='audit_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iam.audituniverseregister'),
        ),
    ]
