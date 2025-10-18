-- Manual SQL script to fix Foreign Key constraint
-- Based on Linus Torvalds' advice: "Fix it directly in the database"
-- 
-- Run this in PostgreSQL production database:
-- psql $DATABASE_URL < fix_fk_constraint_manual.sql

\echo '🔍 Step 1: Check current FK constraints on store_analysis_order.plan_id'
SELECT 
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    confrelid::regclass AS referenced_table,
    pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint
WHERE conrelid = 'store_analysis_order'::regclass 
  AND contype = 'f'
  AND conkey = (SELECT ARRAY[attnum] FROM pg_attribute WHERE attrelid = 'store_analysis_order'::regclass AND attname = 'plan_id');

\echo ''
\echo '🔧 Step 2: Drop ALL FK constraints on plan_id column'
DO $$ 
DECLARE
    constraint_name TEXT;
BEGIN
    FOR constraint_name IN 
        SELECT conname 
        FROM pg_constraint 
        WHERE conrelid = 'store_analysis_order'::regclass 
        AND conkey = (SELECT ARRAY[attnum] FROM pg_attribute WHERE attrelid = 'store_analysis_order'::regclass AND attname = 'plan_id')
        AND contype = 'f'
    LOOP
        EXECUTE 'ALTER TABLE store_analysis_order DROP CONSTRAINT IF EXISTS ' || quote_ident(constraint_name);
        RAISE NOTICE 'Dropped constraint: %', constraint_name;
    END LOOP;
END $$;

\echo ''
\echo '✅ Step 3: Add new FK constraint pointing to ServicePackage'
ALTER TABLE store_analysis_order 
ADD CONSTRAINT store_analysis_order_plan_id_servicepackage_fk 
FOREIGN KEY (plan_id) 
REFERENCES store_analysis_servicepackage(id) 
ON DELETE SET NULL 
DEFERRABLE INITIALLY DEFERRED;

\echo ''
\echo '🎉 Step 4: Verify the new constraint'
SELECT 
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    confrelid::regclass AS referenced_table,
    pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint
WHERE conrelid = 'store_analysis_order'::regclass 
  AND contype = 'f'
  AND conkey = (SELECT ARRAY[attnum] FROM pg_attribute WHERE attrelid = 'store_analysis_order'::regclass AND attname = 'plan_id');

\echo ''
\echo '✅ Done! FK constraint fixed successfully.'

