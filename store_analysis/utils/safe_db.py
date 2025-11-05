#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities برای safe database operations با فیلدهای missing
"""

import logging
from django.db import connection
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def get_available_columns(table_name: str) -> set:
    """دریافت لیست ستون‌های موجود در یک جدول"""
    vendor = connection.vendor
    available_columns = set()
    
    try:
        with connection.cursor() as cursor:
            if vendor == 'postgresql':
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = %s
                """, [table_name])
                available_columns = {row[0] for row in cursor.fetchall()}
            elif vendor == 'sqlite':
                cursor.execute(f"PRAGMA table_info({table_name})")
                available_columns = {row[1] for row in cursor.fetchall()}
    except Exception as e:
        logger.warning(f"Error checking columns for {table_name}: {e}")
    
    return available_columns


def safe_create_store_analysis(**kwargs) -> Any:
    """
    Safe creation of StoreAnalysis object - handles missing fields gracefully
    """
    from store_analysis.models import StoreAnalysis
    
    # فیلدهای اجباری
    required_fields = ['user', 'store_name']
    
    # فیلدهای اختیاری که ممکن است missing باشند یا در model تعریف نشده باشند
    optional_missing_fields = ['store_address', 'package_type', 'contact_phone', 'contact_email', 'priority']
    
    # بررسی فیلدهای موجود
    table_name = 'store_analysis_storeanalysis'
    available_columns = get_available_columns(table_name)
    
    try:
        # ابتدا سعی کن با ORM ایجاد کنی (با حذف فیلدهای missing)
        safe_kwargs = {}
        for key, value in kwargs.items():
            # فیلدهای اجباری را همیشه نگه دار
            if key in required_fields:
                safe_kwargs[key] = value
            # فیلدهای optional missing را از ORM kwargs حذف کن (فقط در raw SQL استفاده می‌شوند)
            elif key in optional_missing_fields:
                # این فیلدها را از ORM kwargs حذف کن - فقط در raw SQL استفاده می‌شوند
                continue
            # سایر فیلدها را فقط اگر ستون موجود باشد نگه دار
            else:
                # تبدیل نام فیلد به نام ستون (معمولاً یکسان است)
                db_field = key
                if db_field in available_columns:
                    safe_kwargs[key] = value
        
        return StoreAnalysis.objects.create(**safe_kwargs)
    except Exception as e:
        # اگر باز هم خطا داشت، از raw SQL استفاده کن
        if 'UndefinedColumn' in str(e) or 'does not exist' in str(e) or 'contact_phone' in str(e) or 'priority' in str(e):
            logger.warning(f"Using raw SQL for StoreAnalysis creation due to: {e}")
            return _create_store_analysis_raw_sql(**kwargs)
        else:
            raise


def _create_store_analysis_raw_sql(**kwargs) -> Any:
    """ایجاد StoreAnalysis با raw SQL"""
    from store_analysis.models import StoreAnalysis
    from django.utils import timezone
    import json
    
    table_name = 'store_analysis_storeanalysis'
    available_columns = get_available_columns(table_name)
    
    # فیلدهای اجباری
    user_id = kwargs.get('user').id if kwargs.get('user') else None
    store_name = kwargs.get('store_name', 'فروشگاه جدید')
    status = kwargs.get('status', 'pending')
    
    # ساخت INSERT statement - فقط فیلدهای موجود
    fields = ['user_id', 'store_name', 'status']
    values = [user_id, store_name, status]
    
    # اضافه کردن analysis_type با مقدار پیش‌فرض (NOT NULL است)
    if 'analysis_type' in available_columns:
        analysis_type_value = kwargs.get('analysis_type', 'comprehensive_7step')  # پیش‌فرض
        fields.append('analysis_type')
        values.append(analysis_type_value)
    
    # اضافه کردن priority با مقدار پیش‌فرض (اگر موجود است و NOT NULL)
    if 'priority' in available_columns:
        priority_value = kwargs.get('priority', 'normal')  # پیش‌فرض: 'normal'
        fields.append('priority')
        values.append(priority_value)
    
    # اضافه کردن package_type با مقدار پیش‌فرض (اگر موجود است و NOT NULL)
    if 'package_type' in available_columns:
        package_type_value = kwargs.get('package_type', 'basic')  # پیش‌فرض: 'basic'
        fields.append('package_type')
        values.append(package_type_value)
    
    # اضافه کردن created_at و updated_at
    if 'created_at' in available_columns:
        fields.append('created_at')
        values.append(timezone.now())
    if 'updated_at' in available_columns:
        fields.append('updated_at')
        values.append(timezone.now())
    
    # اضافه کردن فیلدهای موجود و اختیاری (فقط اگر در available_columns باشند)
    optional_mapping = {
        'store_type': 'store_type',
        'store_size': 'store_size',
        'store_address': 'store_address',
        'final_amount': 'final_amount',
        'additional_info': 'additional_info',
        'business_goals': 'business_goals',
        'marketing_budget': 'marketing_budget',
    }
    
    # فیلدهای missing که نباید اضافه شوند حتی اگر در kwargs باشند
    missing_fields = ['contact_phone', 'contact_email', 'priority']
    
    # اضافه کردن فیلدهای optional که موجود هستند
    for key, db_field in optional_mapping.items():
        # فقط اگر ستون در دیتابیس موجود باشد
        if db_field in available_columns:
            if key in kwargs and kwargs[key] is not None:
                fields.append(db_field)
                values.append(kwargs[key])
            elif db_field in ['store_type', 'store_size']:
                # این فیلدها ممکن است در kwargs نباشند اما در available_columns باشند
                # پس فقط اگر مقدار دارند اضافه می‌شوند
                pass
    
    # contact_phone و contact_email را به صورت جداگانه بررسی کن (اگر موجود باشند)
    # فقط اگر ستون واقعاً در دیتابیس موجود باشد
    for missing_field in ['contact_phone', 'contact_email']:
        # بررسی مجدد که ستون واقعاً موجود است (نه فقط در available_columns)
        if missing_field in available_columns and missing_field in kwargs and kwargs[missing_field] is not None:
            # فقط اضافه کن اگر ستون واقعاً موجود باشد
            try:
                # بررسی نهایی: آیا ستون واقعاً وجود دارد؟
                with connection.cursor() as test_cursor:
                    test_cursor.execute(f"SELECT {connection.ops.quote_name(missing_field)} FROM {connection.ops.quote_name(table_name)} LIMIT 0")
                fields.append(missing_field)
                values.append(kwargs[missing_field])
            except Exception:
                # اگر ستون موجود نیست، skip کن
                logger.debug(f"Skipping {missing_field} - column does not exist in database")
                pass
    
    # اگر analysis_data موجود است و ستون وجود دارد
    if 'analysis_data' in available_columns and 'analysis_data' in kwargs:
        fields.append('analysis_data')
        values.append(json.dumps(kwargs['analysis_data'], ensure_ascii=False))
    
    fields_str = ', '.join([connection.ops.quote_name(f) for f in fields])
    placeholders = ', '.join(['%s'] * len(values))
    
    # متغیر برای نگه‌داری فیلدهای نهایی (در صورت retry)
    final_fields = fields
    
    try:
        with connection.cursor() as cursor:
            quoted_table = connection.ops.quote_name(table_name)
            query = f"""
                INSERT INTO {quoted_table} ({fields_str})
                VALUES ({placeholders})
                RETURNING id
            """
            cursor.execute(query, values)
            analysis_id = cursor.fetchone()[0]
            connection.commit()
    except Exception as insert_error:
        # اگر خطا در INSERT داد، ممکن است فیلدهای missing باشند
        error_str = str(insert_error).lower()
        if 'contact_phone' in error_str or 'contact_email' in error_str or 'does not exist' in error_str:
            # حذف فیلدهای problematic و دوباره تلاش کن
            logger.warning(f"⚠️ Error inserting fields: {insert_error}. Retrying without problematic fields...")
            problematic_fields = ['contact_phone', 'contact_email']
            safe_fields = []
            safe_values = []
            for i, field in enumerate(fields):
                if field not in problematic_fields:
                    safe_fields.append(field)
                    safe_values.append(values[i])
            
            if len(safe_fields) > 0:
                fields_str = ', '.join([connection.ops.quote_name(f) for f in safe_fields])
                placeholders = ', '.join(['%s'] * len(safe_values))
                try:
                    with connection.cursor() as cursor:
                        quoted_table = connection.ops.quote_name(table_name)
                        query = f"""
                            INSERT INTO {quoted_table} ({fields_str})
                            VALUES ({placeholders})
                            RETURNING id
                        """
                        cursor.execute(query, safe_values)
                        analysis_id = cursor.fetchone()[0]
                        connection.commit()
                        # استفاده از safe_fields برای select_fields
                        final_fields = safe_fields
                except Exception as retry_error:
                    logger.error(f"❌ Error in retry insert: {retry_error}")
                    raise
            else:
                raise
        else:
            raise
    
    # استفاده از raw SQL برای خواندن - چون ORM ممکن است فیلدهای missing را بخواند
    # فقط فیلدهای موجود را می‌خوانیم
    select_fields = ['id'] + [f for f in final_fields if f != 'id']
    select_fields_str = ', '.join([connection.ops.quote_name(f) for f in select_fields])
    
    with connection.cursor() as cursor:
        select_query = f"""
            SELECT {select_fields_str}
            FROM {quoted_table}
            WHERE id = %s
        """
        cursor.execute(select_query, [analysis_id])
        row = cursor.fetchone()
        
        # ساخت یک object ساده
        from types import SimpleNamespace
        obj = SimpleNamespace()
        for i, field in enumerate(select_fields):
            if i < len(row):
                setattr(obj, field, row[i])
        
        # تبدیل به StoreAnalysis object با استفاده از _state
        # این کار باعث می‌شود Django فیلدهای missing را ignore کند
        try:
            analysis = StoreAnalysis.objects.raw(f"""
                SELECT {select_fields_str}
                FROM {quoted_table}
                WHERE id = %s
            """, [analysis_id])[0]
            return analysis
        except Exception:
            # اگر raw query هم کار نکرد، از get استفاده کن اما با try-except
            try:
                return StoreAnalysis.objects.get(id=analysis_id)
            except Exception:
                # آخرین راه: ساخت object دستی
                obj.id = analysis_id
                obj.store_name = store_name
                obj.status = status
                # تبدیل به StoreAnalysis instance
                analysis = StoreAnalysis(id=analysis_id)
                for field in select_fields:
                    if hasattr(obj, field):
                        try:
                            setattr(analysis, field, getattr(obj, field))
                        except Exception:
                            pass
                analysis._state.adding = False
                analysis._state.db = connection.alias
                return analysis
    except Exception as e:
        logger.error(f"Error in _create_store_analysis_raw_sql: {e}")
        logger.error(f"Fields: {fields}")
        logger.error(f"Available columns: {available_columns}")
        raise


def safe_get_store_analysis(**filters) -> Optional[Any]:
    """
    Safe retrieval of StoreAnalysis object - handles missing fields
    Returns None if not found or on error
    """
    from store_analysis.models import StoreAnalysis
    
    try:
        # استفاده از Manager که به صورت خودکار defer می‌کند
        return StoreAnalysis.objects.get(**filters)
    except StoreAnalysis.DoesNotExist:
        return None
    except Exception as e:
        if 'contact_phone' in str(e) or 'contact_email' in str(e) or 'UndefinedColumn' in str(e):
            logger.warning(f"Using raw SQL for StoreAnalysis retrieval due to: {e}")
            # استفاده از raw SQL
            return _get_store_analysis_raw_sql(**filters)
        else:
            logger.error(f"Error retrieving StoreAnalysis: {e}")
            raise


def _get_store_analysis_raw_sql(**filters) -> Optional[Any]:
    """دریافت StoreAnalysis با raw SQL"""
    from store_analysis.models import StoreAnalysis
    
    table_name = 'store_analysis_storeanalysis'
    available_columns = get_available_columns(table_name)
    
    # ساخت SELECT statement - فقط فیلدهای موجود
    select_fields = ['id']  # همیشه id وجود دارد
    
    # اضافه کردن فیلدهای موجود
    common_fields = [
        'user_id', 'store_name', 'store_url', 'store_type', 'store_size',
        'store_address', 'additional_info', 'business_goals', 'marketing_budget',
        'analysis_type', 'status', 'package_type', 'final_amount',
        'analysis_data', 'results', 'order_id', 'preliminary_analysis',
        'ai_insights', 'recommendations', 'store_images', 'analysis_files',
        'price', 'currency', 'created_at', 'updated_at', 'completed_at',
        'store_info_id', 'estimated_duration', 'actual_duration',
        'error_message'
    ]
    
    # فقط فیلدهای موجود را اضافه کن
    for field in common_fields:
        if field in available_columns:
            select_fields.append(field)
    
    # اضافه کردن contact_phone و contact_email فقط اگر موجود باشند
    if 'contact_phone' in available_columns:
        select_fields.append('contact_phone')
    if 'contact_email' in available_columns:
        select_fields.append('contact_email')
    if 'priority' in available_columns:
        select_fields.append('priority')
    
    select_fields_str = ', '.join([connection.ops.quote_name(f) for f in select_fields])
    quoted_table = connection.ops.quote_name(table_name)
    
    # ساخت WHERE clause از filters
    where_clauses = []
    values = []
    
    for key, value in filters.items():
        if key == 'pk':
            key = 'id'
        elif key == 'user':
            key = 'user_id'
            value = value.id if hasattr(value, 'id') else value
        elif key == 'id':
            key = 'id'
        
        db_field = key
        if db_field in available_columns or db_field == 'id':
            where_clauses.append(f"{connection.ops.quote_name(db_field)} = %s")
            values.append(value)
    
    if not where_clauses:
        return None
    
    where_clause = ' AND '.join(where_clauses)
    
    try:
        with connection.cursor() as cursor:
            query = f"""
                SELECT {select_fields_str}
                FROM {quoted_table}
                WHERE {where_clause}
                LIMIT 1
            """
            cursor.execute(query, values)
            row = cursor.fetchone()
            
            if not row:
                return None
            
            # ساخت یک object ساده
            from types import SimpleNamespace
            obj = SimpleNamespace()
            for i, field in enumerate(select_fields):
                if i < len(row):
                    setattr(obj, field, row[i])
            
            # تبدیل به StoreAnalysis object
            try:
                analysis = StoreAnalysis.objects.raw(f"""
                    SELECT {select_fields_str}
                    FROM {quoted_table}
                    WHERE {where_clause}
                    LIMIT 1
                """, values)
                
                for a in analysis:
                    return a
                return None
            except Exception:
                # آخرین راه: ساخت object دستی
                analysis = StoreAnalysis(id=obj.id)
                for field in select_fields:
                    if hasattr(obj, field):
                        try:
                            setattr(analysis, field, getattr(obj, field))
                        except Exception:
                            pass
                analysis._state.adding = False
                analysis._state.db = connection.alias
                return analysis
    except Exception as e:
        logger.error(f"Error in _get_store_analysis_raw_sql: {e}")
        return None


def safe_create_userprofile(user, phone: str) -> Any:
    """
    Safe creation of UserProfile object - handles missing birth_date field
    """
    from store_analysis.models import UserProfile
    
    table_name = 'store_analysis_userprofile'
    available_columns = get_available_columns(table_name)
    
    # اگر birth_date موجود نیست، از raw SQL استفاده کن
    if 'birth_date' not in available_columns:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO store_analysis_userprofile (user_id, phone, created_at, updated_at)
                    VALUES (%s, %s, NOW(), NOW())
                    RETURNING id
                """, [user.id, phone])
                profile_id = cursor.fetchone()[0]
                connection.commit()
            
            return UserProfile.objects.get(id=profile_id)
        except Exception as e:
            logger.error(f"Error creating UserProfile with raw SQL: {e}")
            raise
    else:
        # اگر همه فیلدها موجود هستند، از ORM استفاده کن
        return UserProfile.objects.create(user=user, phone=phone)

