# Generated by Django 4.1.2 on 2023-02-15 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_alter_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_photos'),
        ),
    ]