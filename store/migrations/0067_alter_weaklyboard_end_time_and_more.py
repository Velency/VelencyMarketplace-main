from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0066_alter_weaklyboard_end_time_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE store_weaklyboard ALTER COLUMN start_time TYPE timestamp with time zone USING start_time::timestamptz",
            "ALTER TABLE store_weaklyboard ALTER COLUMN start_time TYPE time USING start_time::time"
        ),
        migrations.RunSQL(
            "ALTER TABLE store_weaklyboard ALTER COLUMN end_time TYPE timestamp with time zone USING end_time::timestamptz",
            "ALTER TABLE store_weaklyboard ALTER COLUMN end_time TYPE time USING end_time::time"
        ),
    ]
