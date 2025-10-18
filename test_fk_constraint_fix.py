#!/usr/bin/env python
"""
Test script to verify FK constraint fix
Based on Uncle Bob's Clean Code: "Test everything!"
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.db import connection
from store_analysis.models import Order, ServicePackage
from django.contrib.auth.models import User


def test_fk_constraint_exists():
    """Test 1: Verify FK constraint points to ServicePackage"""
    print("🧪 Test 1: Checking FK constraint...")
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                conname AS constraint_name,
                confrelid::regclass AS referenced_table
            FROM pg_constraint
            WHERE conrelid = 'store_analysis_order'::regclass 
            AND conkey = (SELECT ARRAY[attnum] FROM pg_attribute 
                         WHERE attrelid = 'store_analysis_order'::regclass 
                         AND attname = 'plan_id')
            AND contype = 'f';
        """)
        
        result = cursor.fetchone()
        
        if result:
            constraint_name, referenced_table = result
            print(f"   ✅ FK constraint exists: {constraint_name}")
            print(f"   📍 Points to: {referenced_table}")
            
            if 'servicepackage' in referenced_table.lower():
                print("   ✅ PASS: FK points to ServicePackage")
                return True
            else:
                print(f"   ❌ FAIL: FK points to {referenced_table} instead of ServicePackage")
                return False
        else:
            print("   ❌ FAIL: No FK constraint found!")
            return False


def test_servicepackage_data():
    """Test 2: Verify ServicePackage has data"""
    print("\n🧪 Test 2: Checking ServicePackage data...")
    
    count = ServicePackage.objects.count()
    print(f"   📊 ServicePackage records: {count}")
    
    if count >= 3:
        print("   ✅ PASS: ServicePackage has sufficient data")
        
        for pkg in ServicePackage.objects.all():
            print(f"      - {pkg.name} (ID: {pkg.id}, Type: {pkg.package_type})")
        
        return True
    else:
        print("   ❌ FAIL: ServicePackage needs at least 3 records")
        return False


def test_order_creation():
    """Test 3: Try creating an Order with ServicePackage"""
    print("\n🧪 Test 3: Testing Order creation...")
    
    try:
        # Get first user or create one
        user = User.objects.first()
        if not user:
            print("   ⚠️  No users found, skipping Order creation test")
            return None
        
        # Get basic ServicePackage
        basic_pkg = ServicePackage.objects.filter(package_type='basic').first()
        if not basic_pkg:
            print("   ❌ FAIL: Basic ServicePackage not found")
            return False
        
        # Try creating order (rollback after)
        from django.db import transaction
        
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                plan=basic_pkg,
                order_number=f'TEST-{os.urandom(6).hex()}',
                original_amount=500000,
                base_amount=500000,
                discount_amount=500000,
                final_amount=0,
                status='paid',
                payment_method='test'
            )
            
            print(f"   ✅ PASS: Order created successfully (ID: {order.id})")
            print(f"      - Plan: {order.plan}")
            print(f"      - User: {order.user}")
            
            # Rollback to not affect production
            transaction.set_rollback(True)
            print("   🔄 Test order rolled back (not saved)")
            
        return True
        
    except Exception as e:
        print(f"   ❌ FAIL: {e}")
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("="*60)
    print("🚀 Starting FK Constraint Tests")
    print("="*60)
    
    results = []
    
    results.append(("FK Constraint", test_fk_constraint_exists()))
    results.append(("ServicePackage Data", test_servicepackage_data()))
    results.append(("Order Creation", test_order_creation()))
    
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    
    passed = sum(1 for r in results if r[1] is True)
    failed = sum(1 for r in results if r[1] is False)
    skipped = sum(1 for r in results if r[1] is None)
    
    for test_name, result in results:
        status = "✅ PASS" if result is True else ("❌ FAIL" if result is False else "⚠️  SKIP")
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print("\n🎉 All tests passed! FK constraint is fixed.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)

