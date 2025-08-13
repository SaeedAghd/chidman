from django import forms
from django.core.exceptions import ValidationError
import os
from .models import StoreAnalysis, StoreAnalysisDetail, Payment
from django.core.validators import FileExtensionValidator

class StoreAnalysisForm(forms.ModelForm):
    """
    Form for creating and updating store analyses.
    """
    PRODUCT_CATEGORY_CHOICES = [
        ('groceries', 'مواد غذایی'),
        ('clothing', 'پوشاک'),
        ('electronics', 'الکترونیک'),
        ('home', 'لوازم خانگی'),
        ('beauty', 'لوازم آرایشی و بهداشتی'),
        ('sports', 'ورزشی'),
        ('books', 'کتاب و لوازم تحریر'),
        ('other', 'سایر'),
    ]

    STORE_TYPE_CHOICES = [
        ('supermarket', 'سوپرمارکت'),
        ('hypermarket', 'هایپرمارکت'),
        ('chain', 'فروشگاه زنجیره‌ای'),
        ('clothing', 'پوشاک'),
        ('appliance', 'لوازم خانگی'),
        ('other', 'سایر'),
    ]

    ENTRANCE_CHOICES = [
        ('front', 'جلوی فروشگاه'),
        ('side', 'کنار فروشگاه'),
        ('back', 'پشت فروشگاه'),
        ('multiple', 'چند ورودی'),
    ]

    TRAFFIC_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'زیاد'),
        ('very_high', 'خیلی زیاد'),
    ]

    LIGHTING_CHOICES = [
        ('natural', 'طبیعی'),
        ('artificial', 'مصنوعی'),
        ('mixed', 'ترکیبی'),
    ]

    store_type = forms.ChoiceField(
        choices=STORE_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'نوع فروشگاه'
        })
    )

    main_entrance = forms.ChoiceField(
        choices=ENTRANCE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'ورودی اصلی'
        })
    )

    customer_traffic = forms.ChoiceField(
        choices=TRAFFIC_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'ترافیک مشتری'
        })
    )

    main_lighting = forms.ChoiceField(
        choices=LIGHTING_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'نورپردازی اصلی'
        })
    )

    product_categories = forms.MultipleChoiceField(
        choices=PRODUCT_CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False
    )

    # فیلدهای مربوط به مناطق بلااستفاده
    UNUSED_AREA_CHOICES = [
        ('empty', 'منطقه خالی'),
        ('low_traffic', 'کم‌ترافیک'),
        ('storage', 'انبار'),
        ('staff', 'فضای کارکنان'),
        ('other', 'سایر'),
    ]
    
    # فیلد جدید برای مناطق بلااستفاده چندگانه
    unused_areas_data = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        label='اطلاعات مناطق بلااستفاده'
    )
    
    unused_area_type = forms.CharField(
        required=False,
        label='مناطق بلااستفاده یا کم‌ترافیک',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    unused_area_size = forms.IntegerField(
        min_value=0,
        required=False,
        label='متراژ منطقه بلااستفاده'
    )
    
    unused_area_reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='دلیل بلااستفاده بودن'
    )
    
    unused_areas = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        label='توضیحات تکمیلی مناطق بلااستفاده'
    )

    # فیلدهای مربوط به دوربین نظارتی
    has_surveillance = forms.BooleanField(
        required=False,
        label='آیا دوربین نظارتی دارید؟',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    camera_count = forms.IntegerField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'تعداد دوربین‌ها'}),
        label='تعداد دوربین‌ها'
    )
    
    camera_locations = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'موقعیت دوربین‌ها را توضیح دهید'
        }),
        label='موقعیت دوربین‌ها'
    )
    
    camera_coverage = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'مناطق تحت پوشش دوربین‌ها را توضیح دهید'
        }),
        label='مناطق تحت پوشش'
    )

    # فیلدهای مربوط به ویدیوی مسیر مشتری
    has_customer_video = forms.BooleanField(
        required=False,
        label='آیا ویدیوی مسیر مشتری دارید؟',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    video_duration = forms.IntegerField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'مدت زمان ویدیو (ثانیه)'}),
        label='مدت زمان ویدیو'
    )
    
    video_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='تاریخ ضبط ویدیو'
    )
    
    video_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='ساعت ضبط ویدیو'
    )

    # فیلدهای مربوط به مسیر حرکت مشتری
    customer_movement_paths = forms.ChoiceField(
        choices=[
            ('clockwise', 'ساعتگرد'),
            ('counterclockwise', 'پادساعتگرد'),
            ('mixed', 'مختلط'),
            ('random', 'تصادفی')
        ],
        widget=forms.RadioSelect,
        label='مسیر معمول حرکت مشتریان',
        required=True
    )

    customer_path_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'توضیحات تکمیلی درباره مسیر حرکت مشتریان'
        }),
        label='توضیحات تکمیلی',
        required=True
    )

    morning_sales_percent = forms.IntegerField(label='درصد فروش صبح', min_value=0, max_value=100, required=True)
    noon_sales_percent = forms.IntegerField(label='درصد فروش ظهر', min_value=0, max_value=100, required=True)
    evening_sales_percent = forms.IntegerField(label='درصد فروش عصر', min_value=0, max_value=100, required=True)
    night_sales_percent = forms.IntegerField(label='درصد فروش شب', min_value=0, max_value=100, required=True)

    class Meta:
        model = StoreAnalysis
        fields = [
            'store_name', 'store_location', 'store_type', 'store_size',
            'store_dimensions', 'entrances', 'shelf_count', 'shelf_dimensions',
            'shelf_contents', 'checkout_location', 'unused_areas',
            'product_categories', 'top_products', 'sales_volume',
            'pos_system', 'sales_file', 'has_surveillance', 'camera_count',
            'camera_locations', 'camera_coverage', 'has_customer_video',
            'video_duration', 'video_date', 'video_time', 'customer_movement_paths',
            'customer_path_notes', 'design_style', 'brand_colors',
            'decorative_elements', 'layout_restrictions', 'store_plan',
            'store_photos', 'customer_video_file', 'product_catalog',
            'morning_sales_percent', 'noon_sales_percent', 'evening_sales_percent', 'night_sales_percent',
            'main_entrance', 'customer_traffic', 'main_lighting', 'unused_area_type',
            'unused_area_size', 'unused_area_reason'
        ]
        widgets = {
            'store_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام فروشگاه خود را وارد کنید'}),
            'store_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شهر و منطقه فروشگاه'}),
            'store_type': forms.Select(attrs={'class': 'form-control'}),
            'store_size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متر مربع'}),
            'store_dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: طول = ۱۰م، عرض = ۸م'}),
            'entrances': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'تعداد ورودی‌ها'}),
            
            'shelf_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'shelf_dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ابعاد هر قفسه را وارد کنید'}),
            'shelf_contents': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'محتوای هر قفسه را توضیح دهید'}),
            'checkout_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موقعیت صندوق‌های پرداخت'}),
            'unused_areas': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'مناطق بلااستفاده یا کم‌ترافیک را با جزئیات توضیح دهید'
            }),
            
            'top_products': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'پرفروش‌ترین محصولات را لیست کنید'}),
            'sales_volume': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مثال: 5000000', 'min': '1000000', 'step': '100000'}),
            'pos_system': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام نرم‌افزار صندوق'}),
            'sales_file': forms.FileInput(attrs={'class': 'form-control'}),
            
            'design_style': forms.Select(attrs={'class': 'form-control'}),
            'brand_colors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رنگ‌های اصلی برند را وارد کنید'}),
            'decorative_elements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'عناصر دکوراتیو را توضیح دهید'}),
            'layout_restrictions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'محدودیت‌های چیدمان را توضیح دهید'}),
            
            'store_plan': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.pdf,.dwg'}),
            'store_photos': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'customer_video_file': forms.FileInput(attrs={
                'accept': 'video/mp4,video/avi,video/mov',
                'class': 'form-control'
            }),
            'product_catalog': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'})
        }
        labels = {
            'unused_areas': 'مناطق بلااستفاده',
            'customer_movement_paths': 'مسیر حرکت مشتریان',
            'has_surveillance': 'دوربین نظارتی',
            'customer_video_file': 'ویدیوی مسیر مشتری',
        }

    def clean_store_plan(self):
        file = self.cleaned_data.get('store_plan')
        if file:
            # بررسی پسوند فایل
            import os
            ext = os.path.splitext(file.name)[1].lower()
            allowed_extensions = ['.jpg', '.jpeg', '.pdf', '.dwg']
            
            if ext not in allowed_extensions:
                raise ValidationError(
                    f'فرمت فایل نامعتبر است. فرمت‌های مجاز: {", ".join(allowed_extensions)}'
                )
            
            # بررسی حجم فایل (10MB)
            if file.size > 10 * 1024 * 1024:
                raise ValidationError('حجم فایل نباید از ۱۰ مگابایت بیشتر باشد.')
        
        return file

    def clean_store_photos(self):
        file = self.cleaned_data.get('store_photos')
        if file:
            import os
            ext = os.path.splitext(file.name)[1].lower()
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            
            if ext not in allowed_extensions:
                raise ValidationError(
                    f'فرمت فایل نامعتبر است. فرمت‌های مجاز: {", ".join(allowed_extensions)}'
                )
            
            if file.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('حجم فایل نباید از ۵ مگابایت بیشتر باشد.')
        
        return file

    def clean_customer_video_file(self):
        file = self.cleaned_data.get('customer_video_file')
        if file:
            import os
            ext = os.path.splitext(file.name)[1].lower()
            allowed_extensions = ['.mp4', '.avi', '.mov']
            
            if ext not in allowed_extensions:
                raise ValidationError(
                    f'فرمت فایل نامعتبر است. فرمت‌های مجاز: {", ".join(allowed_extensions)}'
                )
            
            if file.size > 50 * 1024 * 1024:  # 50MB
                raise ValidationError('حجم فایل نباید از ۵۰ مگابایت بیشتر باشد.')
        
        return file

    def clean_product_catalog(self):
        file = self.cleaned_data.get('product_catalog')
        if file:
            # اعتبارسنجی نوع فایل
            allowed_extensions = ['.pdf', '.doc', '.docx']
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError('فقط فایل‌های PDF، DOC و DOCX مجاز هستند.')
            
            # اعتبارسنجی حجم فایل (حداکثر 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('حجم فایل نباید از ۱۰ مگابایت بیشتر باشد.')
        
        return file

    def clean_store_dimensions(self):
        dimensions = self.cleaned_data.get('store_dimensions')
        if dimensions:
            import re
            patterns = [
                r'طول\s*=\s*(\d+)\s*م\s*،\s*عرض\s*=\s*(\d+)\s*م',
                r'طول\s*:\s*(\d+)\s*م\s*،\s*عرض\s*:\s*(\d+)\s*م',
                r'طول\s*(\d+)\s*م\s*،\s*عرض\s*(\d+)\s*م',
                r'(\d+)\s*×\s*(\d+)\s*م',
                r'(\d+)\s*x\s*(\d+)\s*م',
                r'(\d+)\s*م\s*×\s*(\d+)\s*م',
                r'(\d+)\s*m\s*x\s*(\d+)\s*m',
                r'(\d+)\s*m\s*×\s*(\d+)\s*m',
                r'(\d+)\s*x\s*(\d+)',
                r'(\d+)\s*×\s*(\d+)',
            ]
            matched = False
            for pattern in patterns:
                match = re.search(pattern, dimensions)
                if match:
                    matched = True
                    break
            if not matched:
                raise forms.ValidationError('ابعاد باید به یکی از فرمت‌های "10 m x 8 m"، "10m x 8m"، "طول = 10م، عرض = 8م" یا مشابه باشد.')
        return dimensions

    def clean_has_surveillance(self):
        value = self.cleaned_data.get('has_surveillance')
        if isinstance(value, str):
            return value == 'yes' or value is True
        return bool(value)

    def clean_has_customer_video(self):
        value = self.cleaned_data.get('has_customer_video')
        if isinstance(value, str):
            return value == 'yes' or value is True
        return bool(value)

    def clean_sales_volume(self):
        value = self.cleaned_data.get('sales_volume')
        if value in [None, '', [], {}, 'null', 'None']:
            return 0
        return value

    def clean_unused_area_type(self):
        value = self.cleaned_data.get('unused_area_type')
        unused_areas_data = self.cleaned_data.get('unused_areas_data')
        # اگر داده‌های JSON مناطق بلااستفاده وجود دارد، نیازی به این فیلد نیست
        if unused_areas_data and unused_areas_data.strip():
            try:
                import json
                areas = json.loads(unused_areas_data)
                if areas and len(areas) > 0:
                    return value  # مقدار را برگردان حتی اگر خالی باشد
            except (json.JSONDecodeError, TypeError):
                pass
        # اگر مقدار آرایه خالی، None، رشته خالی یا مقدار نامعتبر بود، خطا ایجاد نشود و None بازگردانده شود
        valid_choices = [choice[0] for choice in self.UNUSED_AREA_CHOICES]
        if value in [None, '', [], {}, '[]', 'null', 'None'] or (isinstance(value, list) and len(value) == 0) or value not in valid_choices:
            return None
        return value

    def clean(self):
        cleaned_data = super().clean()
        
        # اعتبارسنجی فیلدهای وابسته به دوربین نظارتی
        has_surveillance = cleaned_data.get('has_surveillance')
        if has_surveillance:
            camera_count = cleaned_data.get('camera_count')
            if not camera_count or camera_count <= 0:
                self.add_error('camera_count', 'در صورت وجود دوربین نظارتی، تعداد دوربین‌ها الزامی است.')
            
            camera_locations = cleaned_data.get('camera_locations')
            if not camera_locations or camera_locations.strip() == '':
                self.add_error('camera_locations', 'در صورت وجود دوربین نظارتی، موقعیت دوربین‌ها الزامی است.')
            
            camera_coverage = cleaned_data.get('camera_coverage')
            if not camera_coverage or camera_coverage.strip() == '':
                self.add_error('camera_coverage', 'در صورت وجود دوربین نظارتی، مناطق تحت پوشش الزامی است.')

        # اعتبارسنجی فیلدهای وابسته به ویدیوی مشتری
        has_customer_video = cleaned_data.get('has_customer_video')
        if has_customer_video:
            video_duration = cleaned_data.get('video_duration')
            if not video_duration or video_duration <= 0:
                self.add_error('video_duration', 'در صورت وجود ویدیوی مشتری، مدت زمان ویدیو الزامی است.')
            
            video_date = cleaned_data.get('video_date')
            if not video_date:
                self.add_error('video_date', 'در صورت وجود ویدیوی مشتری، تاریخ ضبط الزامی است.')

        # اعتبارسنجی دقیق درصدهای فروش
        sales_percentages = [
            ('morning_sales_percent', 'صبح'),
            ('noon_sales_percent', 'ظهر'),
            ('evening_sales_percent', 'عصر'),
            ('night_sales_percent', 'شب')
        ]
        
        total = 0
        for field_name, label in sales_percentages:
            value = cleaned_data.get(field_name, 0)
            if value is None:
                self.add_error(field_name, f'درصد فروش {label} الزامی است.')
                continue
            
            try:
                value = int(value)
                if value < 0 or value > 100:
                    self.add_error(field_name, f'درصد فروش {label} باید بین ۰ تا ۱۰۰ باشد.')
                total += value
            except (ValueError, TypeError):
                self.add_error(field_name, f'درصد فروش {label} باید عدد باشد.')
        
        if total != 100:
            self.add_error(None, f'مجموع درصدهای فروش باید ۱۰۰ باشد. (مجموع فعلی: {total})')

        return cleaned_data

class StoreAnalysisDetailForm(forms.ModelForm):
    class Meta:
        model = StoreAnalysisDetail
        fields = ['store_analysis', 'description', 'recommendations']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'انتخاب کنید'),
                ('online', 'پرداخت آنلاین'),
                ('wallet', 'کیف پول')
            ])
        }