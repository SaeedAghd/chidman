# Complete Production Migration - Fix all missing tables and columns
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0008_aiconsultantservice_pricingplan_transaction_and_more'),
    ]

    operations = [
        # Add currency field to Payment table
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
        
        # Add user field to Payment table if missing
        migrations.RunSQL(
            sql="""
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
            """,
            reverse_sql="ALTER TABLE store_analysis_payment DROP COLUMN IF EXISTS user_id;",
        ),
        
        # Create WalletTransaction table if missing
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS store_analysis_wallettransaction (
                id SERIAL PRIMARY KEY,
                wallet_id INTEGER NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                transaction_type VARCHAR(20) NOT NULL,
                description TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                FOREIGN KEY (wallet_id) REFERENCES store_analysis_wallet(id)
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS store_analysis_wallettransaction;",
        ),
        
        # Create FAQService table if missing
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS store_analysis_faqservice (
                id SERIAL PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category VARCHAR(100),
                is_featured BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS store_analysis_faqservice;",
        ),
    ]
