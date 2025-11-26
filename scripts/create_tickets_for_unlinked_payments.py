#!/usr/bin/env python3
"""
Create SupportTicket records for completed Payments that reference an order_id
but have no matching Order in the DB.
"""
import os
import django
from datetime import timedelta
from django.utils import timezone
import uuid

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chidmano.settings")
django.setup()

from store_analysis.models import Payment, Order, SupportTicket
from django.contrib.auth import get_user_model

User = get_user_model()

def run(days=90, dry_run=False):
    cutoff = timezone.now() - timedelta(days=days)
    payments = Payment.objects.filter(
        created_at__gte=cutoff,
        order_id__isnull=False
    ).exclude(order_id='').filter(status='completed').order_by('-created_at')

    created_tickets = []
    for p in payments:
        if Order.objects.filter(order_number=p.order_id).exists():
            continue

        # Avoid duplicate tickets by searching description for this payment id
        desc_marker = f"Payment {p.id}"
        dup = SupportTicket.objects.filter(description__icontains=desc_marker).first()
        if dup:
            continue

        ticket_user = p.user or User.objects.filter(is_superuser=True).first()
        ticket_id = f"TICK-PAY-{p.id}-{uuid.uuid4().hex[:8].upper()}"
        subject = f"[Auto] پرداخت بدون سفارش: {p.order_id} (پرداخت #{p.id})"
        description = (
            f"پرداختی با شناسه داخلی {p.id} دریافت شده ولی Order متناظر یافت نشد.\n"
            f"User: {getattr(p.user,'id',None)} / {getattr(p.user,'email',None)}\n"
            f"Amount: {p.amount} {p.currency}\n"
            f"Order reference: {p.order_id}\n"
            f"Authority: {p.authority}\n"
            f"Created at: {p.created_at}\n\n"
            "لطفاً بررسی و در صورت نیاز وضعیت مالی/سفارش را همگام‌سازی کنید."
        )

        if dry_run:
            created_tickets.append({'payment_id': p.id, 'ticket_id': ticket_id, 'subject': subject})
            continue

        try:
            t = SupportTicket.objects.create(
                ticket_id=ticket_id,
                user=ticket_user or User.objects.filter(is_superuser=True).first(),
                subject=subject,
                description=description,
                category='billing',
                priority='high',
                attachments=[],
                tags=['auto-ticket', 'payment-no-order']
            )
            created_tickets.append({'payment_id': p.id, 'ticket_id': ticket_id})
            print(f"Created ticket {t.ticket_id} for payment {p.id}")
        except Exception as e:
            print(f"Failed to create ticket for payment {p.id}: {e}")

    print(f"Done. Tickets created: {len(created_tickets)}")
    return created_tickets

if __name__ == '__main__':
    run(days=90, dry_run=False)


