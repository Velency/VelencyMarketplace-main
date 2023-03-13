from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seller',
            old_name='is_verified',
            new_name='verified',
        ),
    ]