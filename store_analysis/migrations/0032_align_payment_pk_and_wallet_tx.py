from django.db import migrations, models


POSTGRES_ADD_WALLET_TX_PAYMENT_ID = r'''
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'store_analysis_wallettransaction' 
          AND column_name = 'payment_id'
    ) THEN
        ALTER TABLE store_analysis_wallettransaction
        ADD COLUMN payment_id bigint NULL;
        ALTER TABLE store_analysis_wallettransaction
        ADD CONSTRAINT store_analysis_wallettransaction_payment_id_fk
        FOREIGN KEY (payment_id) REFERENCES store_analysis_payment(id) ON DELETE SET NULL;
    END IF;
END$$;
'''


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0030_add_missing_fields'),
    ]

    operations = [
        # Align DB schema in production (PostgreSQL). No-op on SQLite; will be faked locally.
        migrations.RunSQL(
            sql=POSTGRES_ADD_WALLET_TX_PAYMENT_ID,
            reverse_sql="""
            -- Keep column; do not drop in reverse to avoid data loss
            """,
            state_operations=[
                migrations.AlterField(
                    model_name='payment',
                    name='id',
                    field=models.BigAutoField(primary_key=True, serialize=False),
                ),
                migrations.AlterField(
                    model_name='wallettransaction',
                    name='payment',
                    field=models.ForeignKey(null=True, blank=True, to='store_analysis.payment', on_delete=models.SET_NULL),
                ),
            ],
        ),
    ]


