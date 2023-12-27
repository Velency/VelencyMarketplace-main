# Generated by Django 4.1.2 on 2023-06-06 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20230603_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=23),
        ),
    ]