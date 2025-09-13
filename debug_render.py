#!/usr/bin/env python
"""
Debug script for Render deployment issues
"""
import os
import sys
import django
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')

try:
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

def check_database():
    """Check database connection"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_static_files():
    """Check static files configuration"""
    try:
        from django.conf import settings
        from django.contrib.staticfiles import finders
        
        print(f"STATIC_URL: {settings.STATIC_URL}")
        print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        
        # Check if static files can be found
        static_files = finders.find('admin/css/base.css')
        if static_files:
            print("✅ Static files configuration OK")
            return True
        else:
            print("⚠️ Static files not found")
            return False
    except Exception as e:
        print(f"❌ Static files check failed: {e}")
        return False

def check_environment():
    """Check environment variables"""
    from django.conf import settings
    
    print("Environment Variables:")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"SECRET_KEY: {'Set' if settings.SECRET_KEY else 'Not Set'}")
    print(f"DATABASE: {settings.DATABASES['default']['ENGINE']}")
    
    # Check if we're in production
    if not settings.DEBUG:
        print("✅ Running in production mode")
    else:
        print("⚠️ Running in debug mode")

def check_migrations():
    """Check if migrations are needed"""
    try:
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        call_command('showmigrations', '--plan', stdout=out)
        migrations = out.getvalue()
        
        if '[ ]' in migrations:
            print("⚠️ Unapplied migrations found")
            print("Run: python manage.py migrate")
            return False
        else:
            print("✅ All migrations applied")
            return True
    except Exception as e:
        print(f"❌ Migration check failed: {e}")
        return False

def create_superuser():
    """Create superuser if needed"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✅ Superuser created: admin/admin123")
        else:
            print("✅ Superuser already exists")
        return True
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False

def main():
    """Run all checks"""
    print("🔍 Running Render deployment checks...\n")
    
    checks = [
        ("Environment", check_environment),
        ("Database", check_database),
        ("Static Files", check_static_files),
        ("Migrations", check_migrations),
        ("Superuser", create_superuser),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n--- {name} Check ---")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed with exception: {e}")
            results.append((name, False))
    
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    failed_checks = [name for name, result in results if not result]
    if failed_checks:
        print(f"\n⚠️ Failed checks: {', '.join(failed_checks)}")
        print("Please fix these issues before deployment.")
        return False
    else:
        print("\n🎉 All checks passed! Ready for deployment.")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
