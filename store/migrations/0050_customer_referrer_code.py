# Generated by Django 4.1.2 on 2023-04-27 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0049_customer_referral_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='referrer_code',
            field=models.CharField(default='', max_length=5),
        ),
    ]
