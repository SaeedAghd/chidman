#!/usr/bin/env python3
"""
Script to run Django migrations automatically
This script should be run on the server after git pull
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def main():
    print("🔄 Running Django migrations...")
    
    try:
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed successfully!")
        
        # Verify migration for client_ip
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='store_analysis_payment' 
                AND column_name='client_ip';
            """)
            result = cursor.fetchone()
            if result:
                print("✅ client_ip column exists in Payment table")
            else:
                print("❌ client_ip column NOT found - migration may have failed")
                sys.exit(1)
        
        # Verify ServicePackage prices
        from store_analysis.models import ServicePackage
        packages = ServicePackage.objects.all()
        print("\n📦 Current ServicePackage prices:")
        for pkg in packages:
            print(f"  - {pkg.package_type}: {pkg.name} - {pkg.price:,} {pkg.currency}")
        
        print("\n✅ Migration verification completed!")
        
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

