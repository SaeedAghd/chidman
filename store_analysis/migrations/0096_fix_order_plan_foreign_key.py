# Generated migration to fix Order.plan foreign key

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0095_alter_promotionalbanner_end_date'),
    ]

    operations = [
        # Remove ALL existing foreign key constraints on plan_id
        migrations.RunSQL(
            sql="""
            DO $$ 
            DECLARE
                constraint_name TEXT;
            BEGIN
                -- Find and drop all FK constraints on plan_id column
                FOR constraint_name IN 
                    SELECT conname 
                    FROM pg_constraint 
                    WHERE conrelid = 'store_analysis_order'::regclass 
                    AND conkey = (SELECT ARRAY[attnum] FROM pg_attribute WHERE attrelid = 'store_analysis_order'::regclass AND attname = 'plan_id')
                    AND contype = 'f'
                LOOP
                    EXECUTE 'ALTER TABLE store_analysis_order DROP CONSTRAINT IF EXISTS ' || quote_ident(constraint_name);
                END LOOP;
            END $$;
            """,
            reverse_sql=migrations.RunSQL.noop
        ),
        
        # Add new foreign key constraint pointing to ServicePackage
        migrations.RunSQL(
            sql="""
            ALTER TABLE store_analysis_order 
            ADD CONSTRAINT store_analysis_order_plan_id_servicepackage_fk 
            FOREIGN KEY (plan_id) 
            REFERENCES store_analysis_servicepackage(id) 
            ON DELETE SET NULL 
            DEFERRABLE INITIALLY DEFERRED;
            """,
            reverse_sql="""
            ALTER TABLE store_analysis_order 
            DROP CONSTRAINT IF EXISTS store_analysis_order_plan_id_servicepackage_fk;
            """
        ),
    ]

