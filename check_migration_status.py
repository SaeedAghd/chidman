#!/usr/bin/env python
"""
Script to check and run pending migrations manually in production
Created based on Guido's advice
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.core.management import call_command
from django.db.migrations.executor import MigrationExecutor
from django.db import connections

def check_migration_status():
    """Check which migrations are applied and which are pending"""
    connection = connections['default']
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    
    print("🔍 Checking migration status...")
    print("-" * 60)
    
    # Get all migrations
    plan = executor.migration_plan(targets)
    
    if not plan:
        print("✅ All migrations are applied!")
        return True
    else:
        print(f"⚠️  Found {len(plan)} pending migrations:")
        for migration, backwards in plan:
            print(f"   - {migration.app_label}.{migration.name}")
        return False

def run_specific_migration():
    """Run migration 0096 specifically"""
    print("\n🔧 Running migration 0096...")
    try:
        call_command('migrate', 'store_analysis', '0096', verbosity=2)
        print("✅ Migration 0096 completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error running migration: {e}")
        return False

if __name__ == '__main__':
    all_applied = check_migration_status()
    
    if not all_applied:
        print("\n" + "="*60)
        run_specific_migration()

