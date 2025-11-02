# Generated manually for safe address field handling
from django.db import migrations, models


def add_address_if_missing(apps, schema_editor):
    """
    Safely add address field to UserProfile if it doesn't exist
    Works with both PostgreSQL (Liara) and SQLite (local dev)
    """
    db_alias = schema_editor.connection.alias
    vendor = schema_editor.connection.vendor
    
    address_exists = False
    
    # Check if column exists based on database vendor
    with schema_editor.connection.cursor() as cursor:
        if vendor == 'postgresql':
            # PostgreSQL uses information_schema
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='store_analysis_userprofile' 
                AND column_name='address'
            """)
            address_exists = cursor.fetchone() is not None
        elif vendor == 'sqlite':
            # SQLite uses PRAGMA table_info
            cursor.execute("PRAGMA table_info(store_analysis_userprofile)")
            columns = [row[1] for row in cursor.fetchall()]
            address_exists = 'address' in columns
    
    # Add address if it doesn't exist
    if not address_exists:
        print("📊 Adding address field to UserProfile...")
        with schema_editor.connection.cursor() as cursor:
            if vendor == 'postgresql':
                cursor.execute("""
                    ALTER TABLE store_analysis_userprofile 
                    ADD COLUMN address TEXT;
                """)
            elif vendor == 'sqlite':
                cursor.execute("""
                    ALTER TABLE store_analysis_userprofile 
                    ADD COLUMN address TEXT;
                """)
        print("✅ address field added")
    else:
        print("ℹ️ address field already exists, skipping...")


def remove_address_safe(apps, schema_editor):
    """
    Reverse migration - remove address field if needed
    """
    db_alias = schema_editor.connection.alias
    vendor = schema_editor.connection.vendor
    
    address_exists = False
    
    # Check if column exists based on database vendor
    with schema_editor.connection.cursor() as cursor:
        if vendor == 'postgresql':
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='store_analysis_userprofile' 
                AND column_name='address'
            """)
            address_exists = cursor.fetchone() is not None
        elif vendor == 'sqlite':
            cursor.execute("PRAGMA table_info(store_analysis_userprofile)")
            columns = [row[1] for row in cursor.fetchall()]
            address_exists = 'address' in columns
    
    with schema_editor.connection.cursor() as cursor:
        if vendor == 'postgresql':
            if address_exists:
                cursor.execute(
                    "ALTER TABLE store_analysis_userprofile DROP COLUMN IF EXISTS address;"
                )
        elif vendor == 'sqlite':
            # SQLite doesn't support DROP COLUMN easily, skip for now
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0116_add_storeanalysis_fields_safe'),
    ]

    operations = [
        migrations.RunPython(add_address_if_missing, remove_address_safe),
    ]

