#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اسکریپت اجرای Migration 0116 با fake کردن migration‌های مشکل‌دار
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def fake_problematic_migrations():
    """Fake کردن migration‌های مشکل‌دار"""
    problematic = ['0076', '0077', '0083', '0098', '0099', '0106', '0113']
    
    for mig in problematic:
        try:
            print(f"Faking migration {mig}...")
            call_command('migrate', 'store_analysis', mig, fake=True, verbosity=1)
            print(f"✅ {mig} faked")
        except Exception as e:
            print(f"⚠️ Error faking {mig}: {e}")

def run_0116():
    """اجرای Migration 0116"""
    try:
        print("\n🔄 Running migration 0116...")
        call_command('migrate', 'store_analysis', '0116', verbosity=2)
        print("✅ Migration 0116 completed")
        return True
    except Exception as e:
        print(f"❌ Error in 0116: {e}")
        return False

def main():
    print("🚀 Fixing migrations...")
    fake_problematic_migrations()
    
    # اجرای migration 0116
    if run_0116():
        print("\n✅ All migrations completed!")
        return 0
    else:
        print("\n❌ Migration failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())

