"""
Management command to create ServicePackage table in production
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Create ServicePackage table if not exists'

    def handle(self, *args, **options):
        self.stdout.write('Creating ServicePackage table...')
        
        with connection.cursor() as cursor:
            # Check if table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_name = 'store_analysis_servicepackage'
                );
            """)
            exists = cursor.fetchone()[0]
            
            if exists:
                self.stdout.write(self.style.SUCCESS('✅ ServicePackage table already exists'))
                return
            
            # Create table
            cursor.execute("""
                CREATE TABLE store_analysis_servicepackage (
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
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS store_analysis_servicepackage_package_type_idx ON store_analysis_servicepackage(package_type);")
            cursor.execute("CREATE INDEX IF NOT EXISTS store_analysis_servicepackage_is_active_idx ON store_analysis_servicepackage(is_active);")
            cursor.execute("CREATE INDEX IF NOT EXISTS store_analysis_servicepackage_price_idx ON store_analysis_servicepackage(price);")
            cursor.execute("CREATE INDEX IF NOT EXISTS store_analysis_servicepackage_sort_order_idx ON store_analysis_servicepackage(sort_order);")
            
            # Insert default packages
            cursor.execute("""
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
            """)
            
            self.stdout.write(self.style.SUCCESS('✅ ServicePackage table created successfully'))
            self.stdout.write(self.style.SUCCESS('✅ Default packages inserted'))

