# Generated manually to fix missing recommendations column

from django.db import migrations, models

def add_recommendations_column_if_not_exists(apps, schema_editor):
    """Add recommendations column if it doesn't exist"""
    if schema_editor.connection.vendor == 'postgresql':
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                   WHERE table_name='store_analysis_storeanalysis' AND column_name='recommendations') THEN
                        ALTER TABLE store_analysis_storeanalysis ADD COLUMN recommendations text NULL;
                    END IF;
                END
                $$;
            """)
    else:
        # For SQLite and other databases, Django's AddField handles it
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0047_add_recommendations_column'),
    ]

    operations = [
        migrations.RunPython(add_recommendations_column_if_not_exists, migrations.RunPython.noop),
        # AddField is safer for Django's internal state, but RunPython handles the actual DB check
        migrations.AddField(
            model_name='storeanalysis',
            name='recommendations',
            field=models.TextField(blank=True, verbose_name='توصیه‌ها'),
        ),
    ]
