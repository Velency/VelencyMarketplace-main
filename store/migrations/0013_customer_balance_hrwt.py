# Generated by Django 4.1.2 on 2023-05-23 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_customer_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='balance_hrwt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
