# Complete Production Migration - Fix all missing tables and columns
from django.db import migrations, models
import django.db.models.deletion
import uuid
from django.db import connection

def run_postgres_sql(apps, schema_editor, sql):
    if schema_editor.connection.vendor == 'postgresql':
        with schema_editor.connection.cursor() as cursor:
            cursor.execute(sql)

def add_currency(apps, schema_editor):
    run_postgres_sql(apps, schema_editor, """
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
""")

def add_user_id(apps, schema_editor):
    run_postgres_sql(apps, schema_editor, """
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'store_analysis_payment' 
        AND column_name = 'user_id'
    ) THEN
        ALTER TABLE store_analysis_payment ADD COLUMN user_id INTEGER REFERENCES auth_user(id);
    END IF;
END $$;
""")

def create_wallet_tx(apps, schema_editor):
    run_postgres_sql(apps, schema_editor, """
CREATE TABLE IF NOT EXISTS store_analysis_wallettransaction (
    id SERIAL PRIMARY KEY,
    wallet_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (wallet_id) REFERENCES store_analysis_wallet(id)
);
""")

def create_faqservice(apps, schema_editor):
    run_postgres_sql(apps, schema_editor, """
CREATE TABLE IF NOT EXISTS store_analysis_faqservice (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(100),
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
""")


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0008_aiconsultantservice_pricingplan_transaction_and_more'),
    ]

    operations = [
        # Add currency field to Payment table
        migrations.RunPython(add_currency, migrations.RunPython.noop),
        
        # Add user field to Payment table if missing
        migrations.RunPython(add_user_id, migrations.RunPython.noop),
        
        # Create WalletTransaction table if missing
        migrations.RunPython(create_wallet_tx, migrations.RunPython.noop),
        
        # Create FAQService table if missing
        migrations.RunPython(create_faqservice, migrations.RunPython.noop),
    ]
