# Generated by Django 4.1.2 on 2023-04-25 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0044_customer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='registred',
            field=models.BooleanField(default=False),
        ),
    ]