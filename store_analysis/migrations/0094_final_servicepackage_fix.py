# Generated manually to fix ServicePackage table issue
# Following Django best practices and expert recommendations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0093_create_servicepackage_model'),
    ]

    operations = [
        # Delete old migration if needed and recreate properly
        migrations.RunSQL(
            # Forward
            sql="""
            -- Drop table if exists (for clean slate)
            DROP TABLE IF EXISTS store_analysis_servicepackage CASCADE;
            
            -- Create table with proper structure
            CREATE TABLE IF NOT EXISTS store_analysis_servicepackage (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                package_type VARCHAR(20) NOT NULL,
                price NUMERIC(10, 2) NOT NULL,
                currency VARCHAR(3) DEFAULT 'IRR' NOT NULL,
                features JSONB DEFAULT '[]'::jsonb,
                max_analyses INTEGER DEFAULT 1 NOT NULL CHECK (max_analyses >= 0),
                validity_days INTEGER DEFAULT 30 NOT NULL CHECK (validity_days >= 0),
                is_active BOOLEAN DEFAULT TRUE NOT NULL,
                is_popular BOOLEAN DEFAULT FALSE NOT NULL,
                sort_order INTEGER DEFAULT 0 NOT NULL CHECK (sort_order >= 0),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            );
            
            -- Create indexes for performance
            CREATE INDEX IF NOT EXISTS store_analysis_servicepackage_package_type_idx 
                ON store_analysis_servicepackage(package_type);
            CREATE INDEX IF NOT EXISTS store_analysis_servicepackage_is_active_idx 
                ON store_analysis_servicepackage(is_active);
            CREATE INDEX IF NOT EXISTS store_analysis_servicepackage_price_idx 
                ON store_analysis_servicepackage(price);
            CREATE INDEX IF NOT EXISTS store_analysis_servicepackage_sort_order_idx 
                ON store_analysis_servicepackage(sort_order);
            
            -- Insert default packages
            INSERT INTO store_analysis_servicepackage 
                (name, description, package_type, price, currency, features, max_analyses, validity_days, is_active, is_popular, sort_order)
            VALUES
                ('تحلیل اولیه', 'تحلیل پایه فروشگاه', 'basic', 0, 'IRR', 
                 '["تحلیل کلی", "5 پیشنهاد", "گزارش 10 صفحه"]'::jsonb, 1, 30, TRUE, FALSE, 1),
                ('تحلیل کامل', 'تحلیل حرفه‌ای فروشگاه', 'professional', 750000, 'IRR', 
                 '["تحلیل جامع", "15 پیشنهاد", "گزارش 25 صفحه", "مشاوره 30 دقیقه"]'::jsonb, 3, 60, TRUE, TRUE, 2),
                ('تحلیل پیشرفته', 'تحلیل سازمانی فروشگاه', 'enterprise', 1500000, 'IRR', 
                 '["تحلیل کامل", "25 پیشنهاد", "گزارش 50 صفحه", "مشاوره 60 دقیقه", "پیگیری 30 روزه"]'::jsonb, 10, 90, TRUE, FALSE, 3)
            ON CONFLICT DO NOTHING;
            """,
            # Reverse
            reverse_sql="DROP TABLE IF EXISTS store_analysis_servicepackage CASCADE;",
        ),
    ]

