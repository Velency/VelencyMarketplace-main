# Generated by Django 4.1.2 on 2024-01-22 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_customer_referrer_code_alter_customer_zipcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='zipcode',
            new_name='city',
        ),
    ]
