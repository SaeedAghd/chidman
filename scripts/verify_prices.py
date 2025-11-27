#!/usr/bin/env python
"""
Script to verify package prices in database
Run: python manage.py shell < scripts/verify_prices.py
Or: python manage.py shell
>>> exec(open('scripts/verify_prices.py').read())
"""
from store_analysis.models import ServicePackage
from decimal import Decimal

print("=" * 60)
print("بررسی قیمت‌های بسته‌های خدمات")
print("=" * 60)

packages = ServicePackage.objects.filter(is_active=True).order_by('sort_order', 'price')

expected_prices = {
    'basic': Decimal('1000000'),  # 1,000,000 Toman
    'professional': Decimal('5000000'),  # 5,000,000 Toman
    'enterprise': Decimal('15000000'),  # 15,000,000 Toman
}

for pkg in packages:
    print(f"\n📦 {pkg.name} ({pkg.package_type})")
    print(f"   قیمت فعلی: {pkg.price:,} {pkg.currency}")
    print(f"   محبوب: {'✅' if pkg.is_popular else '❌'}")
    print(f"   فعال: {'✅' if pkg.is_active else '❌'}")
    
    expected = expected_prices.get(pkg.package_type)
    if expected:
        if pkg.price == expected:
            print(f"   ✅ قیمت صحیح است")
        else:
            print(f"   ❌ قیمت اشتباه است! باید {expected:,} باشد")
            print(f"   🔧 نیاز به اجرای migration 0123")
    
    # Calculate discounted price (80% discount)
    discount_pct = 80
    discounted = pkg.price * (Decimal(100) - Decimal(discount_pct)) / Decimal(100)
    print(f"   قیمت با تخفیف {discount_pct}%: {discounted:,.0f} تومان")

print("\n" + "=" * 60)
print("✅ بررسی کامل شد")
print("=" * 60)

