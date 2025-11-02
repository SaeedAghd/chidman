# 🔧 رفع مشکل Migration 0076

## مشکل:
```
django.db.utils.ProgrammingError: column "authority" of relation "store_analysis_payment" already exists
```

## علت:
Migration 0076 می‌خواهد فیلد `authority` را اضافه کند اما این فیلد از قبل در دیتابیس وجود دارد.

## راه حل:
Fake کردن Migration 0076 چون فیلد از قبل موجود است.

## دستور در Liara Shell:
```bash
python manage.py migrate store_analysis 0076 --fake
```

## سپس ادامه Migration ها:
```bash
python manage.py migrate store_analysis --verbosity=2
```

