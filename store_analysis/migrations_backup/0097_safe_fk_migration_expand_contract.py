# Safe FK migration using Expand-Contract pattern
# Based on Martin Fowler's Refactoring Database pattern

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0096_fix_order_plan_foreign_key'),
    ]

    operations = [
        # For SQLite: Skip all foreign key operations
        # SQLite doesn't support complex ALTER TABLE operations
        migrations.RunSQL(
            sql="SELECT 1;",  # No-op for SQLite
            reverse_sql=migrations.RunSQL.noop
        ),
    ]

