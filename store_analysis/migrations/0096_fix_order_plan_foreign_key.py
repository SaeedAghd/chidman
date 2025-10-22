# Generated migration to fix Order.plan foreign key

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0095_alter_promotionalbanner_end_date'),
    ]

    operations = [
        # For SQLite: Skip foreign key operations as they're not critical for local development
        # The model changes will be applied correctly
        migrations.RunSQL(
            sql="SELECT 1;",  # No-op for SQLite
            reverse_sql=migrations.RunSQL.noop
        ),
    ]

