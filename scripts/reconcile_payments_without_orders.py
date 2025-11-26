#!/usr/bin/env python3
"""
Reconcile payments that have no corresponding Order.
Usage: python scripts/reconcile_payments_without_orders.py
"""
import os
import sys
import django
from decimal import Decimal

# Adjust this if your project uses a different settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chidmano.settings")
django.setup()

from store_analysis.models import Payment, Order
from django.utils import timezone
import logging

logger = logging.getLogger("reconcile")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def reconcile():
    payments = Payment.objects.filter(order_id__isnull=False).exclude(order_id="").filter(
        status__in=['completed', 'processing']
    )
    created = 0
    for p in payments:
        existing_order = Order.objects.filter(order_number=p.order_id).first()
        if existing_order:
            continue
        try:
            order = Order.objects.create(
                order_number=p.order_id,
                user=p.user,
                status='paid' if p.status == 'completed' else 'pending',
                original_amount=p.amount or Decimal('0.00'),
                base_amount=p.amount or Decimal('0.00'),
                final_amount=p.amount or Decimal('0.00'),
                currency=p.currency or 'IRR',
                payment=p,
                payment_method=p.payment_method or 'ping_payment',
                created_at=timezone.now(),
            )
            created += 1
            logger.info(f"Created Order {order.order_number} for Payment {p.id} (status={p.status})")
        except Exception as e:
            logger.error(f"Failed to create order for Payment {p.id}: {e}")

    logger.info(f"Done. Created {created} orders.")


if __name__ == "__main__":
    reconcile()


