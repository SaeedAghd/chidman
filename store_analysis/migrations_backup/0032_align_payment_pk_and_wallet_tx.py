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

    def add_wallet_tx_payment_id(apps, schema_editor):
        if schema_editor.connection.vendor == 'postgresql':
            with schema_editor.connection.cursor() as cursor:
                cursor.execute(POSTGRES_ADD_WALLET_TX_PAYMENT_ID)

    operations = [
        # Align DB schema in production (PostgreSQL). No-op on SQLite.
        migrations.RunPython(add_wallet_tx_payment_id, migrations.RunPython.noop),
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
    ]


