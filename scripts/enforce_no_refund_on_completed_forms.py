import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chidmano.settings")
django.setup()

from store_analysis.models import Payment, Order, StoreAnalysis
from django.utils import timezone
import logging

logger = logging.getLogger("enforce_no_refund")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)

def run():
    logger.info("Scanning payments to enforce 'no refund if form completed' policy...")
    payments = Payment.objects.filter(status__in=['pending', 'failed']).select_related('store_analysis', 'user')
    updated = 0
    for p in payments:
        sa = getattr(p, 'store_analysis', None)
        if not sa:
            continue
        sa_status = getattr(sa, 'status', None)
        analysis_data = sa.analysis_data or {}
        form_completed = False
        if sa_status in ('processing', 'completed'):
            form_completed = True
        elif isinstance(analysis_data, dict) and analysis_data.get('uploaded_files'):
            form_completed = True

        if form_completed:
            logger.info("Marking payment %s completed because analysis %s status=%s", p.id, sa.id, sa_status)
            p.status = 'completed'
            p.completed_at = timezone.now()
            try:
                p.save(update_fields=['status', 'completed_at'])
            except Exception as e:
                logger.error("Failed to save payment %s: %s", p.id, e)
                continue

            # ensure order is paid
            try:
                order = Order.objects.filter(order_number=p.order_id).first()
                if order and order.status != 'paid':
                    order.status = 'paid'
                    order.payment = p
                    order.transaction_id = p.transaction_id or p.authority
                    order.save(update_fields=['status', 'payment', 'transaction_id'])
            except Exception as e:
                logger.error("Failed to update order for payment %s: %s", p.id, e)

            updated += 1

    logger.info("Done. Payments updated: %d", updated)

if __name__ == "__main__":
    run()


