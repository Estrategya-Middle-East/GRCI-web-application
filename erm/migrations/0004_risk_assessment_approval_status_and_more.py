# Generated by Django 5.1.1 on 2024-11-28 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erm', '0003_remove_risk_created_at_alter_risk_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='risk',
            name='assessment_approval_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('under_review', 'Under Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=50),
        ),
        migrations.AddField(
            model_name='risk',
            name='define_approval_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('under_review', 'Under Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='riskass',
            name='approval_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('under_review', 'Under Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='riskdefine',
            name='approval_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('under_review', 'Under Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=50),
        ),
    ]
