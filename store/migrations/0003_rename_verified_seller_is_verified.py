# Generated by Django 4.1.2 on 2023-03-13 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_verified_seller_is_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seller',
            old_name='verified',
            new_name='is_verified',
        ),
    ]