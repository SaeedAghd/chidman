# Generated manually for safe field addition
from django.db import migrations, models


def add_fields_safe(apps, schema_editor):
    """
    Safely add package_type and store_address fields to StoreAnalysis
    This migration checks if columns exist before adding them
    Works with both PostgreSQL (Liara) and SQLite (local dev)
    """
    db_alias = schema_editor.connection.alias
    vendor = schema_editor.connection.vendor
    
    package_type_exists = False
    store_address_exists = False
    
    # Check if columns exist based on database vendor
    with schema_editor.connection.cursor() as cursor:
        if vendor == 'postgresql':
            # PostgreSQL uses information_schema
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='store_analysis_storeanalysis' 
                AND column_name='package_type'
            """)
            package_type_exists = cursor.fetchone() is not None
            
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='store_analysis_storeanalysis' 
                AND column_name='store_address'
            """)
            store_address_exists = cursor.fetchone() is not None
        elif vendor == 'sqlite':
            # SQLite uses PRAGMA table_info
            cursor.execute("PRAGMA table_info(store_analysis_storeanalysis)")
            columns = [row[1] for row in cursor.fetchall()]
            package_type_exists = 'package_type' in columns
            store_address_exists = 'store_address' in columns
    
    # Add package_type if it doesn't exist
    if not package_type_exists:
        print("📊 Adding package_type field to StoreAnalysis...")
        with schema_editor.connection.cursor() as cursor:
            if vendor == 'postgresql':
                cursor.execute("""
                    ALTER TABLE store_analysis_storeanalysis 
                    ADD COLUMN package_type VARCHAR(20) DEFAULT 'basic';
                """)
                # Make it NOT NULL after setting default for existing rows
                cursor.execute("""
                    ALTER TABLE store_analysis_storeanalysis 
                    ALTER COLUMN package_type SET NOT NULL;
                """)
            elif vendor == 'sqlite':
                cursor.execute("""
                    ALTER TABLE store_analysis_storeanalysis 
                    ADD COLUMN package_type VARCHAR(20) DEFAULT 'basic' NOT NULL;
                """)
        print("✅ package_type field added")
    else:
        print("ℹ️ package_type field already exists, skipping...")
    
    # Add store_address if it doesn't exist
    if not store_address_exists:
        print("📊 Adding store_address field to StoreAnalysis...")
        with schema_editor.connection.cursor() as cursor:
            if vendor == 'postgresql':
                cursor.execute("""
                    ALTER TABLE store_analysis_storeanalysis 
                    ADD COLUMN store_address TEXT;
                """)
            elif vendor == 'sqlite':
                cursor.execute("""
                    ALTER TABLE store_analysis_storeanalysis 
                    ADD COLUMN store_address TEXT;
                """)
        print("✅ store_address field added")
    else:
        print("ℹ️ store_address field already exists, skipping...")


def remove_fields_safe(apps, schema_editor):
    """
    Reverse migration - remove fields if needed
    """
    db_alias = schema_editor.connection.alias
    vendor = schema_editor.connection.vendor
    
    package_type_exists = False
    store_address_exists = False
    
    # Check if columns exist based on database vendor
    with schema_editor.connection.cursor() as cursor:
        if vendor == 'postgresql':
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='store_analysis_storeanalysis' 
                AND column_name='package_type'
            """)
            package_type_exists = cursor.fetchone() is not None
            
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='store_analysis_storeanalysis' 
                AND column_name='store_address'
            """)
            store_address_exists = cursor.fetchone() is not None
        elif vendor == 'sqlite':
            cursor.execute("PRAGMA table_info(store_analysis_storeanalysis)")
            columns = [row[1] for row in cursor.fetchall()]
            package_type_exists = 'package_type' in columns
            store_address_exists = 'store_address' in columns
    
    with schema_editor.connection.cursor() as cursor:
        if vendor == 'postgresql':
            if package_type_exists:
                cursor.execute(
                    "ALTER TABLE store_analysis_storeanalysis DROP COLUMN IF EXISTS package_type;"
                )
            if store_address_exists:
                cursor.execute(
                    "ALTER TABLE store_analysis_storeanalysis DROP COLUMN IF EXISTS store_address;"
                )
        elif vendor == 'sqlite':
            # SQLite doesn't support DROP COLUMN easily, skip for now
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0115_add_review_reminder_model'),
    ]

    operations = [
        migrations.RunPython(
            add_fields_safe,
            reverse_code=remove_fields_safe,
            atomic=False  # Allow partial execution
        ),
    ]
