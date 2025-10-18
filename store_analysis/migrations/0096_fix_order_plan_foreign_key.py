# Generated migration to fix Order.plan foreign key

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0095_alter_promotionalbanner_end_date'),
    ]

    operations = [
        # Remove old foreign key constraint pointing to PricingPlan
        migrations.RunSQL(
            sql="""
            ALTER TABLE store_analysis_order 
            DROP CONSTRAINT IF EXISTS store_analysis_order_plan_id_e7ea3ab7_fk_store_ana;
            """,
            reverse_sql=migrations.RunSQL.noop
        ),
        
        # Add new foreign key constraint pointing to ServicePackage
        migrations.RunSQL(
            sql="""
            ALTER TABLE store_analysis_order 
            ADD CONSTRAINT store_analysis_order_plan_id_fkey 
            FOREIGN KEY (plan_id) 
            REFERENCES store_analysis_servicepackage(id) 
            ON DELETE SET NULL 
            DEFERRABLE INITIALLY DEFERRED;
            """,
            reverse_sql="""
            ALTER TABLE store_analysis_order 
            DROP CONSTRAINT IF EXISTS store_analysis_order_plan_id_fkey;
            """
        ),
    ]

