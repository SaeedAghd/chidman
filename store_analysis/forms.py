from django import forms
from django.core.exceptions import ValidationError
from .models import StoreAnalysis, Payment
import re

# --- فرم اصلی تحلیل فروشگاه ---
class StoreAnalysisForm(forms.ModelForm):
    """فرم اصلی تحلیل فروشگاه"""
    
    # اضافه کردن فیلدهای مورد نیاز برای فرم ساده
    store_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام فروشگاه'})
    )
    
    store_size = forms.IntegerField(
        min_value=50,
        max_value=10000,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مساحت فروشگاه (متر مربع)'})
    )

    store_type = forms.ChoiceField(
        choices=[
            ('retail', 'خرده فروشی'),
        ('supermarket', 'سوپرمارکت'),
        ('hypermarket', 'هایپرمارکت'),
            ('convenience', 'فروشگاه راحتی'),
            ('specialty', 'فروشگاه تخصصی'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'})
    )

    class Meta:
        model = StoreAnalysis
        fields = ['status', 'priority', 'estimated_duration']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'estimated_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مدت زمان تخمینی (دقیقه)'})
        }

# --- فرم تحلیل هوشمند فروشگاه ---
class AIStoreAnalysisForm(forms.Form):
    """فرم تحلیل هوشمند فروشگاه"""
    
    # Basic Info
    store_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام فروشگاه'})
    )
    
    store_size = forms.IntegerField(
        min_value=50,
        max_value=10000,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مساحت فروشگاه (متر مربع)'})
    )

    store_type = forms.ChoiceField(
        choices=[
            ('retail', 'خرده فروشی'),
            ('supermarket', 'سوپرمارکت'),
            ('hypermarket', 'هایپرمارکت'),
            ('convenience', 'فروشگاه راحتی'),
            ('specialty', 'فروشگاه تخصصی'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # اطلاعات تکمیلی فروشگاه
    store_location = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'آدرس کامل فروشگاه'})
    )
    
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شهر'})
    )
    
    area = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'منطقه یا محله'})
    )
    
    establishment_year = forms.IntegerField(
        min_value=1300,
        max_value=1450,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سال تاسیس (1300-1450)'})
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تماس'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'})
    )
    
    # Layout Analysis
    entrance_count = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'تعداد ورودی‌ها'})
    )
    
    checkout_count = forms.IntegerField(
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'تعداد صندوق‌ها'})
    )
    
    shelf_count = forms.IntegerField(
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'تعداد قفسه‌ها'})
    )
    
    # اطلاعات دقیق‌تر چیدمان
    shelf_dimensions = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ابعاد تقریبی هر قفسه (مثال: 2×1.5 متر)'})
    )
    
    shelf_contents = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'توضیح نوع محصولات موجود در هر قفسه...'})
    )
    
    unused_area_size = forms.IntegerField(
        min_value=0,
        max_value=10000,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متراژ مناطق بلااستفاده'})
    )
    
    unused_area_type = forms.ChoiceField(
        choices=[
        ('empty', 'منطقه خالی'),
        ('low_traffic', 'کم‌ترافیک'),
        ('storage', 'انبار'),
        ('staff', 'فضای کارکنان'),
        ('maintenance', 'نگهداری'),
        ('delivery', 'تحویل'),
            ('other', 'سایر')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    main_lighting = forms.ChoiceField(
        choices=[
            ('natural', 'نور طبیعی'),
            ('artificial', 'مصنوعی'),
            ('mixed', 'ترکیبی'),
        ],
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    # طراحی و دکوراسیون
    design_style = forms.ChoiceField(
        choices=[
            ('traditional', 'سنتی'),
            ('modern', 'مدرن'),
            ('minimal', 'مینیمال'),
            ('luxury', 'لوکس'),
            ('industrial', 'صنعتی'),
            ('scandinavian', 'اسکاندیناوی'),
            ('vintage', 'کلاسیک'),
            ('contemporary', 'معاصر'),
            ('other', 'سایر'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    brand_colors = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رنگ‌های اصلی برند (مثال: آبی، سفید، طلایی)'})
    )
    
    lighting_intensity = forms.ChoiceField(
        choices=[
            ('low', 'کم'),
            ('medium', 'متوسط'),
            ('high', 'زیاد'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Customer Behavior
    customer_dwell_time = forms.IntegerField(
        min_value=5,
        max_value=180,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متوسط زمان حضور مشتری (دقیقه)'})
    )
    
    conversion_rate = forms.DecimalField(
        min_value=1,
        max_value=100,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'نرخ تبدیل (درصد)', 'step': '0.1'})
    )
    
    stopping_points = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('entrance', 'ورودی فروشگاه'),
            ('promotions', 'قسمت تخفیف‌ها'),
            ('new_products', 'محصولات جدید'),
            ('checkout', 'صندوق‌ها'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='نقاط توقف مشتریان'
    )
    
    customer_paths = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('clockwise', 'در جهت عقربه‌های ساعت'),
            ('counterclockwise', 'خلاف عقربه‌های ساعت'),
            ('random', 'تصادفی'),
            ('direct', 'مستقیم به هدف'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='مسیرهای معمول مشتریان'
    )

    high_traffic_areas = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'مناطقی که بیشترین ترافیک را دارند...'})
    )
    
    # Traffic Analysis
    customer_traffic = forms.IntegerField(
        min_value=10,
        max_value=10000,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متوسط تعداد مشتری روزانه'})
    )
    
    peak_hours = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ساعات پیک فروش (مثال: 18-22)'})
    )
    
    peak_days = forms.MultipleChoiceField(
        choices=[
            ('monday', 'دوشنبه'),
            ('tuesday', 'سه‌شنبه'),
            ('wednesday', 'چهارشنبه'),
            ('thursday', 'پنج‌شنبه'),
            ('friday', 'جمعه'),
            ('saturday', 'شنبه'),
            ('sunday', 'یکشنبه'),
        ],
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='روزهای شلوغ هفته'
    )
    
    morning_sales_percent = forms.IntegerField(
        min_value=0,
        max_value=100,
        initial=30,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'درصد فروش صبح (6-12)'})
    )
    
    noon_sales_percent = forms.IntegerField(
        min_value=0,
        max_value=100,
        initial=40,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'درصد فروش ظهر (12-18)'})
    )
    
    evening_sales_percent = forms.IntegerField(
        min_value=0,
        max_value=100,
        initial=30,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'درصد فروش شب (18-24)'})
    )
    
    # محصولات و فروش
    product_categories = forms.MultipleChoiceField(
        choices=[
            ('beverages', 'نوشیدنی'),
            ('food', 'خوراکی'),
            ('womens_clothing', 'پوشاک زنانه'),
            ('mens_clothing', 'پوشاک مردانه'),
            ('kids_clothing', 'پوشاک بچگانه'),
            ('electronics', 'الکترونیک'),
            ('home', 'لوازم خانگی'),
            ('beauty', 'آرایشی و بهداشتی'),
            ('books', 'کتاب'),
            ('pharmacy', 'دارویی'),
            ('sports', 'ورزشی'),
            ('jewelry', 'جواهرات'),
            ('other', 'سایر'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='دسته‌بندی محصولات'
    )
    
    top_products = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'لیست محصولات پرفروش...'})
    )
    
    daily_sales_volume = forms.DecimalField(
        max_digits=15,
        decimal_places=0,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متوسط فروش روزانه (تومان)'})
    )
    
    supplier_count = forms.IntegerField(
        min_value=0,
        max_value=1000,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'تعداد تامین‌کنندگان'})
    )
    
    # نظارت و امنیت
    has_surveillance = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='دوربین نظارتی'
    )
    
    camera_count = forms.IntegerField(
        min_value=0,
        max_value=100,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'تعداد دوربین‌ها'})
    )
    
    camera_locations = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'توضیح موقعیت نصب دوربین‌ها...'})
    )
    
    # آپلود فایل‌ها و تصاویر
    store_photos = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        help_text='عکس کلی فروشگاه (حداکثر 10MB)'
    )
    
    store_plan = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf,.dwg'}),
        help_text='نقشه یا طرح فروشگاه (PDF, DWG, تصویر)'
    )
    
    shelf_photos = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        help_text='عکس قفسه‌ها و چیدمان'
    )
    
    entrance_photos = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        help_text='عکس ورودی‌ها و ویترین‌ها'
    )
    
    checkout_photos = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        help_text='عکس صندوق‌ها و منطقه پرداخت'
    )
    
    customer_video = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
        help_text='ویدیوی مسیر حرکت مشتریان (حداکثر 50MB)'
    )
    
    surveillance_footage = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
        help_text='نمونه فیلم دوربین نظارتی (حداکثر 50MB)'
    )
    
    # اطلاعات ویدیو
    video_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text='تاریخ ضبط ویدیو'
    )
    
    video_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        help_text='ساعت ضبط ویدیو'
    )
    
    video_duration = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=3600,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مدت زمان ویدیو (ثانیه)'}),
        help_text='مدت زمان ویدیو به ثانیه'
    )
    
    # اطلاعات فایل فروش
    sales_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx,.xls,.csv,.pdf'}),
        help_text='فایل گزارش فروش (Excel, CSV, PDF)'
    )
    
    product_catalog = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
        help_text='کاتالوگ محصولات (PDF, Word)'
    )
    
    # اطلاعات نرم‌افزاری
    pos_system = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام نرم‌افزار صندوق (مثال: سما، رایان، راهکار)'})
    )
    
    inventory_system = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نرم‌افزار مدیریت موجودی'})
    )
    
    # Optimization
    sales_improvement_target = forms.IntegerField(
        min_value=5,
        max_value=100,
        initial=20,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'هدف بهبود فروش (%)'})
    )
    
    optimization_timeline = forms.IntegerField(
        min_value=1,
        max_value=24,
        initial=6,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'بازه زمانی هدف (ماه)'})
    )
    
    optimization_types = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('layout', 'بهینه‌سازی چیدمان'),
            ('pricing', 'استراتژی قیمت‌گذاری'),
            ('inventory', 'مدیریت موجودی'),
            ('staffing', 'بهینه‌سازی نیروی انسانی'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='نوع بهینه‌سازی مورد نیاز'
    )
    
    # Sales Prediction
    historical_data_months = forms.IntegerField(
        min_value=3,
        max_value=60,
        initial=12,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'داده‌های تاریخی فروش (ماه)'})
    )
    
    prediction_period = forms.ChoiceField(
        choices=[
            ('', 'انتخاب کنید'),
            ('1', '1 ماه آینده'),
            ('3', '3 ماه آینده'),
            ('6', '6 ماه آینده'),
            ('12', '1 سال آینده'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='دوره پیش‌بینی'
    )
    
    seasonal_patterns = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('spring', 'فصل بهار'),
            ('summer', 'فصل تابستان'),
            ('autumn', 'فصل پاییز'),
            ('winter', 'فصل زمستان'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='الگوهای فصلی'
    )
    
    prediction_accuracy = forms.ChoiceField(
        choices=[
            ('high', 'دقت بالا (95%+) - زمان پردازش بیشتر'),
            ('medium', 'دقت متوسط (85-95%) - تعادل مناسب'),
            ('low', 'دقت پایین (75-85%) - سرعت بالا'),
        ],
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='دقت پیش‌بینی مورد انتظار'
    )
    
    # Final Report
    analyst_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام تحلیلگر'})
    )
    
    report_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل برای دریافت گزارش'})
    )
    
    contact_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تماس'})
    )
    
    report_deadline = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    report_types = forms.MultipleChoiceField(
        choices=[
            ('pdf', 'PDF جامع'),
            ('excel', 'فایل Excel'),
            ('presentation', 'ارائه پاورپوینت'),
            ('dashboard', 'داشبورد تعاملی'),
        ],
        initial=['pdf'],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='نوع گزارش'
    )
    
    additional_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'هرگونه توضیح یا درخواست خاص برای تحلیل...'})
    )
    
    notifications = forms.MultipleChoiceField(
        choices=[
            ('email', 'ایمیل'),
            ('sms', 'پیامک'),
            ('whatsapp', 'واتساپ'),
        ],
        initial=['email'],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='نحوه اطلاع‌رسانی'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate sales percentages sum to 100
        morning = cleaned_data.get('morning_sales_percent', 0)
        noon = cleaned_data.get('noon_sales_percent', 0)
        evening = cleaned_data.get('evening_sales_percent', 0)
        
        if morning and noon and evening:
            total = morning + noon + evening
            if total != 100:
                raise ValidationError('مجموع درصدهای فروش باید 100 باشد')
        
        # Validate camera count if surveillance is enabled
        has_surveillance = cleaned_data.get('has_surveillance')
        camera_count = cleaned_data.get('camera_count')
        if has_surveillance and not camera_count:
            raise ValidationError('در صورت داشتن دوربین، تعداد دوربین‌ها الزامی است')
        
        # Validate unused area size
        store_size = cleaned_data.get('store_size')
        unused_area_size = cleaned_data.get('unused_area_size')
        if store_size and unused_area_size and unused_area_size > store_size:
            raise ValidationError('منطقه بلااستفاده نمی‌تواند بزرگتر از کل فروشگاه باشد')
        
        # Validate file sizes
        files_to_check = [
            'store_photos', 'shelf_photos', 'entrance_photos', 'checkout_photos',
            'store_plan', 'sales_file', 'product_catalog'
        ]
        
        for file_field in files_to_check:
            file_obj = cleaned_data.get(file_field)
            if file_obj and hasattr(file_obj, 'size'):
                if file_obj.size > 10 * 1024 * 1024:  # 10MB
                    raise ValidationError(f'حجم فایل {file_field} نباید بیش از 10 مگابایت باشد')
        
        # Validate video files (50MB limit)
        video_files = ['customer_video', 'surveillance_footage']
        for video_field in video_files:
            video_obj = cleaned_data.get(video_field)
            if video_obj and hasattr(video_obj, 'size'):
                if video_obj.size > 50 * 1024 * 1024:  # 50MB
                    raise ValidationError(f'حجم ویدیو {video_field} نباید بیش از 50 مگابایت باشد')
        
        # Validate video metadata
        customer_video = cleaned_data.get('customer_video')
        video_date = cleaned_data.get('video_date')
        video_time = cleaned_data.get('video_time')
        video_duration = cleaned_data.get('video_duration')
        
        if customer_video and not video_date:
            raise ValidationError('در صورت آپلود ویدیو، تاریخ ضبط الزامی است')
        
        return cleaned_data

# --- فرم پرداخت ---
class PaymentForm(forms.ModelForm):
    """فرم پرداخت"""
    
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مبلغ (تومان)'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise ValidationError('مبلغ باید بیشتر از صفر باشد')
        return amount
