# Safe FK migration using Expand-Contract pattern
# Based on Martin Fowler's Refactoring Database pattern

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0096_fix_order_plan_foreign_key'),
    ]

    operations = [
        # EXPAND Phase: Allow both old and new references temporarily
        migrations.RunSQL(
            sql="""
            -- Step 1: Make plan_id nullable temporarily to allow data migration
            ALTER TABLE store_analysis_order ALTER COLUMN plan_id DROP NOT NULL;
            """,
            reverse_sql="ALTER TABLE store_analysis_order ALTER COLUMN plan_id SET NOT NULL;"
        ),
        
        # CONTRACT Phase: Remove old constraint if migration 0096 didn't work
        migrations.RunSQL(
            sql="""
            -- Step 2: Drop any remaining FK constraints on plan_id
            DO $$ 
            DECLARE
                r RECORD;
            BEGIN
                FOR r IN 
                    SELECT constraint_name
                    FROM information_schema.table_constraints
                    WHERE table_name = 'store_analysis_order'
                    AND constraint_type = 'FOREIGN KEY'
                    AND constraint_name LIKE '%plan_id%'
                LOOP
                    EXECUTE 'ALTER TABLE store_analysis_order DROP CONSTRAINT IF EXISTS ' || quote_ident(r.constraint_name);
                END LOOP;
            END $$;
            """,
            reverse_sql=migrations.RunSQL.noop
        ),
        
        # FINALIZE Phase: Add correct FK constraint
        migrations.RunSQL(
            sql="""
            -- Step 3: Ensure ServicePackage table exists and has data
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM store_analysis_servicepackage LIMIT 1) THEN
                    RAISE NOTICE 'WARNING: store_analysis_servicepackage table is empty!';
                END IF;
            END $$;
            
            -- Step 4: Add new FK constraint to ServicePackage
            ALTER TABLE store_analysis_order 
            ADD CONSTRAINT store_analysis_order_plan_servicepackage_fk 
            FOREIGN KEY (plan_id) 
            REFERENCES store_analysis_servicepackage(id) 
            ON DELETE SET NULL 
            DEFERRABLE INITIALLY DEFERRED;
            
            -- Step 5: Create index for performance
            CREATE INDEX IF NOT EXISTS idx_order_plan_servicepackage 
            ON store_analysis_order(plan_id) 
            WHERE plan_id IS NOT NULL;
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_order_plan_servicepackage;
            ALTER TABLE store_analysis_order DROP CONSTRAINT IF EXISTS store_analysis_order_plan_servicepackage_fk;
            """
        ),
    ]

