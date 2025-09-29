# Simple migration for Production - Only add currency field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0008_aiconsultantservice_pricingplan_transaction_and_more'),
    ]

    operations = [
        # Simple SQL to add currency field
        migrations.RunSQL(
            sql="""
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'store_analysis_payment' 
                    AND column_name = 'currency'
                ) THEN
                    ALTER TABLE store_analysis_payment ADD COLUMN currency VARCHAR(3) DEFAULT 'IRR';
                END IF;
            END $$;
            """,
            reverse_sql="ALTER TABLE store_analysis_payment DROP COLUMN IF EXISTS currency;",
        ),
    ]
