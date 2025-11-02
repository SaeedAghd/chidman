# اسکریپت PowerShell برای اجرای Migration در Liara Shell
# Usage: .\liara_migrate.ps1

Write-Host "🚀 اتصال به Liara Shell و اجرای Migration" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# بررسی وجود Liara CLI
if (-not (Get-Command liara -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Liara CLI نصب نشده است!" -ForegroundColor Red
    Write-Host "📦 نصب با: npm install -g @liara/cli" -ForegroundColor Yellow
    exit 1
}

# بررسی لاگین
Write-Host "🔐 بررسی احراز هویت..." -ForegroundColor Yellow
$whoami = liara whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  لطفاً لاگین کنید:" -ForegroundColor Yellow
    liara login
}

Write-Host ""
Write-Host "📋 گزینه‌های موجود:" -ForegroundColor Green
Write-Host "1. اجرای Migration 0116 (فقط store_address و package_type)" -ForegroundColor White
Write-Host "2. اجرای تمام Migration ها" -ForegroundColor White
Write-Host "3. بررسی وضعیت Migration ها" -ForegroundColor White
Write-Host "4. باز کردن Shell دستی" -ForegroundColor White
Write-Host ""
$choice = Read-Host "لطفاً گزینه مورد نظر را انتخاب کنید (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🔄 اجرای Migration 0116..." -ForegroundColor Yellow
        liara shell -c "python manage.py migrate store_analysis 0116 --verbosity=2"
    }
    "2" {
        Write-Host ""
        Write-Host "🔄 اجرای تمام Migration ها..." -ForegroundColor Yellow
        liara shell -c "python manage.py migrate --verbosity=2"
    }
    "3" {
        Write-Host ""
        Write-Host "📊 بررسی وضعیت Migration ها..." -ForegroundColor Yellow
        liara shell -c "python manage.py showmigrations store_analysis"
    }
    "4" {
        Write-Host ""
        Write-Host "🐚 باز کردن Shell دستی..." -ForegroundColor Yellow
        Write-Host "💡 بعد از اتصال، دستورات زیر را اجرا کنید:" -ForegroundColor Cyan
        Write-Host "   python manage.py migrate store_analysis 0116" -ForegroundColor White
        Write-Host "   python manage.py migrate" -ForegroundColor White
        Write-Host "   exit" -ForegroundColor White
        liara shell
    }
    default {
        Write-Host "❌ گزینه نامعتبر!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✅ انجام شد!" -ForegroundColor Green

