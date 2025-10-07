from django.db import migrations, models

def add_store_images_column_if_not_exists(apps, schema_editor):
    """Safely add store_images column if it doesn't exist"""
    db_engine = schema_editor.connection.vendor
    
    if db_engine == 'postgresql':
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='store_analysis_storeanalysis' AND column_name='store_images') THEN
                        ALTER TABLE store_analysis_storeanalysis ADD COLUMN store_images jsonb DEFAULT '[]'::jsonb;
                    END IF;
                END
                $$;
            """)
    else:
        # For SQLite and other databases, Django's AddField handles it
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0048_add_recommendations_safe'),
    ]

    operations = [
        migrations.RunPython(add_store_images_column_if_not_exists, migrations.RunPython.noop),
        # AddField is safer for Django's internal state, but RunPython handles the actual DB check
        migrations.AddField(
            model_name='storeanalysis',
            name='store_images',
            field=models.JSONField(default=list, verbose_name='تصاویر فروشگاه'),
        ),
    ]
