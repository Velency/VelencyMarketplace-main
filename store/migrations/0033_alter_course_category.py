# Generated by Django 4.1.2 on 2023-11-19 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_alter_course_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='Category',
            field=models.CharField(choices=[('1', 'Основные курсы'), ('2', 'Занятие телом'), ('3', 'Игры')], default='Основные курсы', max_length=20),
        ),
    ]
