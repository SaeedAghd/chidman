# Migration for Production - Fix Payment table currency field
# This migration adds the missing currency field to Payment table

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0008_aiconsultantservice_pricingplan_transaction_and_more'),
    ]

    operations = [
        # Add currency field to Payment model
        migrations.RunSQL(
            sql="ALTER TABLE store_analysis_payment ADD COLUMN currency VARCHAR(3) DEFAULT 'IRR';",
            reverse_sql="ALTER TABLE store_analysis_payment DROP COLUMN currency;",
        ),
        # Add user field to Payment model if missing
        migrations.RunSQL(
            sql="ALTER TABLE store_analysis_payment ADD COLUMN user_id INTEGER REFERENCES auth_user(id);",
            reverse_sql="ALTER TABLE store_analysis_payment DROP COLUMN user_id;",
        ),
    ]
