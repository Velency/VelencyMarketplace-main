# Generated by Django 4.1.2 on 2023-12-06 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0036_direction_sale_name_alter_direction_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('end_date', models.DateField()),
                ('customers', models.ManyToManyField(to='store.customer')),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.direction')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.direction')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.BooleanField()),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.direction')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.purchase')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
            ],
        ),
        migrations.CreateModel(
            name='lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('zoom_link', models.URLField()),
                ('zoom_rec', models.URLField()),
                ('homework', models.TextField()),
                ('teachers', models.ManyToManyField(to='store.teammember')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='lesson',
            field=models.ManyToManyField(to='store.lesson'),
        ),
    ]