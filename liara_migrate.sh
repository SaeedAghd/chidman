#!/bin/bash
# اسکریپت اجرای Migration در Liara Shell
# Usage: ./liara_migrate.sh

echo "🚀 اتصال به Liara Shell و اجرای Migration"
echo "=========================================="
echo ""

# بررسی وجود Liara CLI
if ! command -v liara &> /dev/null; then
    echo "❌ Liara CLI نصب نشده است!"
    echo "📦 نصب با: npm install -g @liara/cli"
    exit 1
fi

# بررسی لاگین
echo "🔐 بررسی احراز هویت..."
if ! liara whoami &> /dev/null; then
    echo "⚠️  لطفاً لاگین کنید:"
    liara login
fi

echo ""
echo "📋 گزینه‌های موجود:"
echo "1. اجرای Migration 0116 (فقط store_address و package_type)"
echo "2. اجرای تمام Migration ها"
echo "3. بررسی وضعیت Migration ها"
echo "4. باز کردن Shell دستی"
echo ""
read -p "لطفاً گزینه مورد نظر را انتخاب کنید (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🔄 اجرای Migration 0116..."
        liara shell -c "python manage.py migrate store_analysis 0116 --verbosity=2"
        ;;
    2)
        echo ""
        echo "🔄 اجرای تمام Migration ها..."
        liara shell -c "python manage.py migrate --verbosity=2"
        ;;
    3)
        echo ""
        echo "📊 بررسی وضعیت Migration ها..."
        liara shell -c "python manage.py showmigrations store_analysis"
        ;;
    4)
        echo ""
        echo "🐚 باز کردن Shell دستی..."
        echo "💡 بعد از اتصال، دستورات زیر را اجرا کنید:"
        echo "   python manage.py migrate store_analysis 0116"
        echo "   python manage.py migrate"
        echo "   exit"
        liara shell
        ;;
    *)
        echo "❌ گزینه نامعتبر!"
        exit 1
        ;;
esac

echo ""
echo "✅ انجام شد!"

