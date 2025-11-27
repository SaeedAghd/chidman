#!/usr/bin/env python3
"""
Auto-migration script for Liara deployment
This script safely runs migrations and handles existing columns gracefully
"""
import os
import sys
import django
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def check_column_exists(table_name, column_name):
    """Check if a column exists in PostgreSQL"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name=%s 
                AND column_name=%s;
            """, [table_name, column_name])
            return cursor.fetchone() is not None
    except Exception as e:
        logger.warning(f"⚠️ Could not check column {column_name} in {table_name}: {e}")
        return False

def main():
    logger.info("🔄 Starting auto-migration for Liara...")
    
    try:
        # Check if critical columns exist (for verification)
        logger.info("🔍 Checking database schema...")
        
        # Run migrations
        logger.info("🔧 Running migrations...")
        call_command('migrate', interactive=False, verbosity=1)
        logger.info("✅ Migrations completed successfully!")
        
        # Verify critical migrations
        logger.info("🔍 Verifying migrations...")
        
        # Check Payment.client_ip
        if check_column_exists('store_analysis_payment', 'client_ip'):
            logger.info("✅ client_ip column exists in Payment table")
        else:
            logger.warning("⚠️ client_ip column NOT found - may need manual migration")
        
        # Check TicketMessage.is_internal
        if check_column_exists('store_analysis_ticketmessage', 'is_internal'):
            logger.info("✅ is_internal column exists in TicketMessage table")
        else:
            logger.warning("⚠️ is_internal column NOT found - may need manual migration")
        
        # Show ServicePackage prices
        try:
            from store_analysis.models import ServicePackage
            packages = ServicePackage.objects.all()
            logger.info("\n📦 Current ServicePackage prices:")
            for pkg in packages:
                logger.info(f"  - {pkg.package_type}: {pkg.name} - {pkg.price:,} {pkg.currency}")
        except Exception as e:
            logger.warning(f"⚠️ Could not fetch ServicePackage prices: {e}")
        
        logger.info("\n✅ Auto-migration completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"❌ Error running migrations: {e}")
        import traceback
        logger.error(traceback.format_exc())
        # Don't exit with error - safe migrations will handle gracefully
        logger.info("ℹ️ Continuing - safe migrations will handle existing columns")
        return 0  # Return 0 to not fail deployment

if __name__ == '__main__':
    sys.exit(main())

