# Generated by Django 4.1.2 on 2024-01-19 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='referrer_code',
            field=models.CharField(blank=True, default='Academy', max_length=5),
        ),
    ]
