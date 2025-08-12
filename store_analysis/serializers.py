from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StoreAnalysis, Payment, StoreAnalysisResult, Cache

class UserSerializer(serializers.ModelSerializer):
    """Serializer برای کاربر"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class StoreAnalysisSerializer(serializers.ModelSerializer):
    """Serializer برای تحلیل فروشگاه"""
    user = serializers.ReadOnlyField(source='user.username')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    store_type_display = serializers.CharField(source='get_store_type_display', read_only=True)
    
    class Meta:
        model = StoreAnalysis
        fields = [
            'id', 'user', 'store_name', 'store_location', 'store_type', 'store_type_display',
            'store_size', 'store_dimensions', 'status', 'status_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class StoreAnalysisDetailSerializer(serializers.ModelSerializer):
    """Serializer برای جزئیات تحلیل فروشگاه"""
    user = serializers.ReadOnlyField(source='user.username')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    store_type_display = serializers.CharField(source='get_store_type_display', read_only=True)
    
    class Meta:
        model = StoreAnalysis
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    """Serializer برای پرداخت‌ها"""
    user = serializers.ReadOnlyField(source='user.username')
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'amount', 'payment_method', 'payment_method_display',
            'status', 'status_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class AnalysisStatsSerializer(serializers.Serializer):
    """Serializer برای آمار تحلیل‌ها"""
    total_analyses = serializers.IntegerField()
    completed_analyses = serializers.IntegerField()
    processing_analyses = serializers.IntegerField()
    failed_analyses = serializers.IntegerField()
    average_score = serializers.FloatField()
    total_payments = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)

class CacheSerializer(serializers.ModelSerializer):
    """Serializer برای کش"""
    cache_type_display = serializers.CharField(source='get_cache_type_display', read_only=True)
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = Cache
        fields = [
            'id', 'key', 'value', 'cache_type', 'cache_type_display',
            'expires_at', 'created_at', 'updated_at', 'is_expired'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_is_expired(self, obj):
        """بررسی انقضای کش"""
        return obj.is_expired()

class FileUploadSerializer(serializers.Serializer):
    """Serializer برای آپلود فایل"""
    file = serializers.FileField()
    file_type = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=255, required=False)
    
    def validate_file(self, value):
        """اعتبارسنجی فایل"""
        from ..services.security_service import FileSecurityValidator
        
        # بررسی اندازه فایل
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError('اندازه فایل نباید بیشتر از 10 مگابایت باشد.')
        
        # بررسی پسوند فایل
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx']
        file_name = value.name.lower()
        if not any(file_name.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError('پسوند فایل مجاز نیست.')
        
        # بررسی محتوای فایل
        if not FileSecurityValidator.validate_file_content(value):
            raise serializers.ValidationError('نوع فایل نامعتبر است.')
        
        return value

class SearchSerializer(serializers.Serializer):
    """Serializer برای جستجو"""
    query = serializers.CharField(max_length=255)
    filters = serializers.DictField(required=False)
    page = serializers.IntegerField(min_value=1, required=False)
    page_size = serializers.IntegerField(min_value=1, max_value=100, required=False)

class AnalysisCreateSerializer(serializers.ModelSerializer):
    """Serializer برای ایجاد تحلیل"""
    files = serializers.ListField(child=FileUploadSerializer(), required=False)
    
    class Meta:
        model = StoreAnalysis
        fields = [
            'store_name', 'store_type', 'store_location', 'city', 'area',
            'store_size', 'store_dimensions', 'description', 'has_surveillance',
            'camera_count', 'camera_locations', 'camera_coverage',
            'has_customer_video', 'video_duration', 'video_date',
            'morning_sales_percentage', 'noon_sales_percentage',
            'evening_sales_percentage', 'night_sales_percentage',
            'files'
        ]
    
    def validate(self, data):
        """اعتبارسنجی داده‌ها"""
        # بررسی فیلدهای اجباری
        required_fields = ['store_name', 'store_type', 'store_location', 'store_size']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f'فیلد {field} الزامی است.')
        
        # بررسی درصدهای فروش
        sales_fields = [
            'morning_sales_percentage', 'noon_sales_percentage',
            'evening_sales_percentage', 'night_sales_percentage'
        ]
        total = sum(data.get(field, 0) for field in sales_fields)
        if total != 100:
            raise serializers.ValidationError('مجموع درصدهای فروش باید 100 باشد.')
        
        return data
    
    def create(self, validated_data):
        """ایجاد تحلیل جدید"""
        files = validated_data.pop('files', [])
        analysis = StoreAnalysis.objects.create(**validated_data)
        
        # پردازش فایل‌ها
        for file_data in files:
            file_obj = file_data['file']
            file_type = file_data['file_type']
            
            if file_type == 'store_plan':
                analysis.store_plan = file_obj
            elif file_type == 'store_photos':
                analysis.store_photos = file_obj
            elif file_type == 'customer_video':
                analysis.customer_video_file = file_obj
            elif file_type == 'product_catalog':
                analysis.product_catalog = file_obj
        
        analysis.save()
        return analysis

class AnalysisUpdateSerializer(serializers.ModelSerializer):
    """Serializer برای به‌روزرسانی تحلیل"""
    files = serializers.ListField(child=FileUploadSerializer(), required=False)
    
    class Meta:
        model = StoreAnalysis
        fields = [
            'store_name', 'store_type', 'store_location', 'city', 'area',
            'store_size', 'store_dimensions', 'description', 'has_surveillance',
            'camera_count', 'camera_locations', 'camera_coverage',
            'has_customer_video', 'video_duration', 'video_date',
            'morning_sales_percentage', 'noon_sales_percentage',
            'evening_sales_percentage', 'night_sales_percentage',
            'files'
        ]
    
    def update(self, instance, validated_data):
        """به‌روزرسانی تحلیل"""
        files = validated_data.pop('files', [])
        
        # به‌روزرسانی فیلدها
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # پردازش فایل‌های جدید
        for file_data in files:
            file_obj = file_data['file']
            file_type = file_data['file_type']
            
            if file_type == 'store_plan':
                instance.store_plan = file_obj
            elif file_type == 'store_photos':
                instance.store_photos = file_obj
            elif file_type == 'customer_video':
                instance.customer_video_file = file_obj
            elif file_type == 'product_catalog':
                instance.product_catalog = file_obj
        
        instance.save()
        return instance 