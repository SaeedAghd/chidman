from django.db import migrations, connection


def add_ai_insights_column(apps, schema_editor):
    with connection.cursor() as cursor:
        try:
            cursor.execute("PRAGMA table_info('store_analysis_storeanalysis')")
            columns = [row[1] for row in cursor.fetchall()]  # row[1] is the column name in SQLite
        except Exception:
            columns = []

        if 'ai_insights' not in columns:
            try:
                cursor.execute("ALTER TABLE store_analysis_storeanalysis ADD COLUMN ai_insights TEXT")
            except Exception:
                # If DB is PostgreSQL/MySQL, attempt a generic add
                schema_editor.execute(
                    "ALTER TABLE store_analysis_storeanalysis ADD COLUMN ai_insights TEXT"
                )


def noop_reverse(apps, schema_editor):
    # Intentionally left empty; dropping columns is destructive and varies by DB
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("store_analysis", "0044_alter_promotionalbanner_end_date"),
    ]

    operations = [
        migrations.RunPython(add_ai_insights_column, noop_reverse),
    ]


