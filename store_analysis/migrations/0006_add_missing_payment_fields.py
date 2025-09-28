# Generated manually to fix production issues

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0005_userprofile'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE store_analysis_payment ADD COLUMN IF NOT EXISTS order_id VARCHAR(100);",
            reverse_sql="ALTER TABLE store_analysis_payment DROP COLUMN IF EXISTS order_id;"
        ),
        migrations.RunSQL(
            "ALTER TABLE store_analysis_payment ADD COLUMN IF NOT EXISTS payment_id VARCHAR(100);",
            reverse_sql="ALTER TABLE store_analysis_payment DROP COLUMN IF EXISTS payment_id;"
        ),
        migrations.RunSQL(
            "ALTER TABLE store_analysis_payment ADD COLUMN IF NOT EXISTS gateway_response JSONB;",
            reverse_sql="ALTER TABLE store_analysis_payment DROP COLUMN IF EXISTS gateway_response;"
        ),
        migrations.RunSQL(
            "ALTER TABLE store_analysis_payment ADD COLUMN IF NOT EXISTS transaction_id VARCHAR(100);",
            reverse_sql="ALTER TABLE store_analysis_payment DROP COLUMN IF EXISTS transaction_id;"
        ),
        migrations.RunSQL(
            "ALTER TABLE store_analysis_payment ADD COLUMN IF NOT EXISTS is_test BOOLEAN DEFAULT FALSE;",
            reverse_sql="ALTER TABLE store_analysis_payment DROP COLUMN IF EXISTS is_test;"
        ),
        migrations.RunSQL(
            "ALTER TABLE store_analysis_wallet ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'IRR';",
            reverse_sql="ALTER TABLE store_analysis_wallet DROP COLUMN IF EXISTS currency;"
        ),
        migrations.RunSQL(
            "ALTER TABLE store_analysis_storeanalysis ADD COLUMN IF NOT EXISTS store_url VARCHAR(500);",
            reverse_sql="ALTER TABLE store_analysis_storeanalysis DROP COLUMN IF EXISTS store_url;"
        ),
        migrations.RunSQL(
            "ALTER TABLE store_analysis_supportticket ADD COLUMN IF NOT EXISTS resolved_at TIMESTAMP;",
            reverse_sql="ALTER TABLE store_analysis_supportticket DROP COLUMN IF EXISTS resolved_at;"
        ),
        migrations.RunSQL(
            "ALTER TABLE store_analysis_supportticket ADD COLUMN IF NOT EXISTS closed_at TIMESTAMP;",
            reverse_sql="ALTER TABLE store_analysis_supportticket DROP COLUMN IF EXISTS closed_at;"
        ),
        migrations.RunSQL(
            "ALTER TABLE store_analysis_supportticket ADD COLUMN IF NOT EXISTS last_reply_at TIMESTAMP;",
            reverse_sql="ALTER TABLE store_analysis_supportticket DROP COLUMN IF EXISTS last_reply_at;"
        ),
    ]
