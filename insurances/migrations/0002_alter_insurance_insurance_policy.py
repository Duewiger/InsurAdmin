# Generated by Django 5.0.4 on 2024-05-24 18:47

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurance',
            name='insurance_policy',
            field=models.FileField(blank=True, upload_to="insurance_policies"),
        ),
    ]
