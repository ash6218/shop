# Generated by Django 5.2.1 on 2025-08-01 12:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_address_user_birthday_user_national_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='national_id',
            field=models.CharField(blank=True, default='', max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='please enter exactly 10 digits number', regex='^\\d{10}$')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='please enter exactly 10 digits number', regex='^\\d{10}$')]),
        ),
    ]
