# Generated by Django 5.1.1 on 2024-12-05 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erm', '0024_alter_oversight_supportingdocuments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corevaluesmonitoring',
            name='SupportingEvidence',
            field=models.FileField(blank=True, null=True, upload_to='corevaluesmonitoring_docs/'),
        ),
        migrations.AlterField(
            model_name='oversight',
            name='SupportingDocuments',
            field=models.FileField(blank=True, null=True, upload_to='oversight_docs/'),
        ),
    ]
