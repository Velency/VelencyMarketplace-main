# Generated by Django 4.1.2 on 2023-12-24 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0057_stream_open_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='open_status',
            field=models.BooleanField(default=False),
        ),
    ]