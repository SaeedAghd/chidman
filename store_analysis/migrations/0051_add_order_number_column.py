from django.db import migrations, models

def add_order_number_column_if_not_exists(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='store_analysis_order' AND column_name='order_number') THEN
                    ALTER TABLE store_analysis_order ADD COLUMN order_number varchar(50) NULL;
                END IF;
            END
            $$;
            """
        )

class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0050_storeanalysis_priority_alter_order_id_and_more'),
    ]

    operations = [
        migrations.RunPython(add_order_number_column_if_not_exists, migrations.RunPython.noop),
    ]
