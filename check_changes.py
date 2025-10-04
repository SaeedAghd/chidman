#!/usr/bin/env python
"""
تست سریع برای بررسی تغییرات
"""

def check_payment_template():
    """بررسی فایل template"""
    print("🔍 بررسی فایل template صفحه پرداخت\n")
    
    try:
        with open('store_analysis/templates/store_analysis/payment_page.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # بررسی عناصر کلیدی
        checks = [
            ('order.final_amount == 0', 'شرط مبلغ صفر'),
            ('rechargeWallet()', 'تابع شارژ کیف پول'),
            ('proceedWithFreeAnalysis()', 'تابع تحلیل رایگان'),
            ('شارژ کیف پول', 'دکمه شارژ کیف پول'),
            ('ادامه با تحلیل رایگان', 'دکمه تحلیل رایگان'),
            ('به مناسبت افتتاحیه', 'پیام تخفیف'),
            ('zero-amount-section', 'بخش مبلغ صفر'),
        ]
        
        print("📋 بررسی عناصر کلیدی:")
        all_found = True
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description}")
                all_found = False
        
        if all_found:
            print("\n🎉 تمام تغییرات در فایل موجود است!")
            print("✅ Template آماده است")
        else:
            print("\n❌ برخی تغییرات موجود نیست!")
        
        # بررسی ساختار کلی
        print(f"\n📊 آمار فایل:")
        print(f"   - تعداد خطوط: {len(content.splitlines())}")
        print(f"   - حجم فایل: {len(content)} کاراکتر")
        
        # بررسی بخش مبلغ صفر
        if 'zero-amount-section' in content:
            print(f"   - بخش مبلغ صفر: ✅ موجود")
        else:
            print(f"   - بخش مبلغ صفر: ❌ موجود نیست")
        
        return all_found
        
    except Exception as e:
        print(f"❌ خطا در خواندن فایل: {e}")
        return False

def check_views_changes():
    """بررسی تغییرات views"""
    print("\n🔍 بررسی تغییرات views.py\n")
    
    try:
        with open('store_analysis/views.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # بررسی تغییرات کلیدی
        checks = [
            ('تخفیف 100% برای تمام کاربران', 'تخفیف 100%'),
            ('discount = total', 'محاسبه تخفیف'),
            ('discount_percentage = 100', 'درصد تخفیف'),
            ('final_amount = Decimal(\'0\')', 'مبلغ نهایی صفر'),
            ('order.final_amount == 0', 'شرط مبلغ صفر در پردازش'),
        ]
        
        print("📋 بررسی تغییرات views:")
        all_found = True
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description}")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"❌ خطا در خواندن فایل: {e}")
        return False

def main():
    """تابع اصلی"""
    print("🚀 بررسی سریع تغییرات\n")
    
    template_ok = check_payment_template()
    views_ok = check_views_changes()
    
    print(f"\n🎯 نتیجه نهایی:")
    print(f"   - Template: {'✅' if template_ok else '❌'}")
    print(f"   - Views: {'✅' if views_ok else '❌'}")
    
    if template_ok and views_ok:
        print(f"\n🎉 همه تغییرات اعمال شده است!")
        print(f"✅ مشکل احتمالاً در cache یا server است")
        print(f"\n💡 راه‌حل‌های پیشنهادی:")
        print(f"   1. Django server را restart کنید")
        print(f"   2. Cache مرورگر را پاک کنید (Ctrl+F5)")
        print(f"   3. حالت incognito/private استفاده کنید")
        print(f"   4. python manage.py runserver را دوباره اجرا کنید")
    else:
        print(f"\n❌ برخی تغییرات اعمال نشده است!")
    
    return template_ok and views_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
