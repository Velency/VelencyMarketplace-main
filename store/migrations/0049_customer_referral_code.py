# Generated by Django 4.1.2 on 2023-04-27 18:50

from django.db import migrations, models
import secrets


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0048_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='referral_code',
            field=models.CharField(default=secrets.token_urlsafe, max_length=5, unique=True),
        ),
    ]
