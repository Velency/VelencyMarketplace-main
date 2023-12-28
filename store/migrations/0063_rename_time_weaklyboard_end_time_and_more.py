# Generated by Django 4.1.2 on 2023-12-27 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0062_weaklyboard'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weaklyboard',
            old_name='time',
            new_name='end_time',
        ),
        migrations.AddField(
            model_name='weaklyboard',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
