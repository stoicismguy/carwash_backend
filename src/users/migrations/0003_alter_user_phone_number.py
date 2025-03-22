# Generated by Django 5.1.7 on 2025-03-22 04:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть 11 цифр, например: 79001234567', regex='^\\d{11}$')], verbose_name='Номер телефона'),
        ),
    ]
