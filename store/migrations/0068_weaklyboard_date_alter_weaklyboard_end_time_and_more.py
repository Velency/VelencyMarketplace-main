# Generated by Django 4.1.2 on 2023-12-27 19:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0067_alter_weaklyboard_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='weaklyboard',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='weaklyboard',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='weaklyboard',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]