from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0009_complete_production_fix'),
    ]

    operations = [
        # Add columns if missing (safe for prod), and sync Django state
        migrations.RunSQL(
            sql=(
                """
                ALTER TABLE store_analysis_payment
                ADD COLUMN IF NOT EXISTS description text;
                """
            ),
            reverse_sql="""
                -- irreversible safely; keep column
            """,
            state_operations=[
                migrations.AlterField(
                    model_name='payment',
                    name='description',
                    field=models.TextField(null=True, blank=True),
                ),
            ],
        ),
        migrations.RunSQL(
            sql=(
                """
                ALTER TABLE store_analysis_wallettransaction
                ADD COLUMN IF NOT EXISTS description text;
                """
            ),
            reverse_sql="""
                -- irreversible safely; keep column
            """,
            state_operations=[
                migrations.AlterField(
                    model_name='wallettransaction',
                    name='description',
                    field=models.TextField(null=True, blank=True),
                ),
            ],
        ),
        migrations.RunSQL(
            sql=(
                """
                ALTER TABLE store_analysis_faqservice
                ADD COLUMN IF NOT EXISTS sort_order integer DEFAULT 0 NOT NULL;
                """
            ),
            reverse_sql="""
                -- irreversible safely; keep column
            """,
            state_operations=[
                migrations.AlterField(
                    model_name='faqservice',
                    name='sort_order',
                    field=models.IntegerField(default=0),
                ),
            ],
        ),
    ]