from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0009_complete_production_fix'),
    ]

    def add_payment_description(apps, schema_editor):
        if schema_editor.connection.vendor == 'postgresql':
            with schema_editor.connection.cursor() as cursor:
                cursor.execute("ALTER TABLE store_analysis_payment ADD COLUMN IF NOT EXISTS description text;")

    def add_wallettx_description(apps, schema_editor):
        if schema_editor.connection.vendor == 'postgresql':
            with schema_editor.connection.cursor() as cursor:
                cursor.execute("ALTER TABLE store_analysis_wallettransaction ADD COLUMN IF NOT EXISTS description text;")

    def add_faqservice_sort_order(apps, schema_editor):
        if schema_editor.connection.vendor == 'postgresql':
            with schema_editor.connection.cursor() as cursor:
                cursor.execute("ALTER TABLE store_analysis_faqservice ADD COLUMN IF NOT EXISTS sort_order integer DEFAULT 0 NOT NULL;")

    operations = [
        # Add columns if missing (safe for prod); RunPython ensures Postgres-only execution
        migrations.RunPython(add_payment_description, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='payment',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.RunPython(add_wallettx_description, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='wallettransaction',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.RunPython(add_faqservice_sort_order, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='faqservice',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
    ]