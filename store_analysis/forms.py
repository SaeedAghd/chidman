from django import forms
from django.core.exceptions import ValidationError
from .models import StoreAnalysis, Payment
import re

# --- فرم اصلی تحلیل فروشگاه ---
class StoreAnalysisForm(forms.ModelForm):
    """فرم اصلی تحلیل فروشگاه"""
    
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
    
    main_lighting = forms.ChoiceField(
        choices=[
            ('natural', 'نور طبیعی'),
            ('artificial', 'مصنوعی'),
            ('mixed', 'ترکیبی'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    # Customer Behavior
    customer_dwell_time = forms.IntegerField(
        min_value=5,
        max_value=180,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متوسط زمان حضور مشتری (دقیقه)'})
    )
    
    conversion_rate = forms.DecimalField(
        min_value=1,
        max_value=100,
        decimal_places=2,
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
    
    # Traffic Analysis
    customer_traffic = forms.IntegerField(
        min_value=10,
        max_value=10000,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متوسط تعداد مشتری روزانه'})
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
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='روزهای شلوغ هفته'
    )
    
    morning_sales_percent = forms.IntegerField(
        min_value=0,
        max_value=100,
        initial=30,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'درصد فروش صبح (6-12)'})
    )
    
    noon_sales_percent = forms.IntegerField(
        min_value=0,
        max_value=100,
        initial=40,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'درصد فروش ظهر (12-18)'})
    )
    
    evening_sales_percent = forms.IntegerField(
        min_value=0,
        max_value=100,
        initial=30,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'درصد فروش شب (18-24)'})
    )
    
    # Optimization
    sales_improvement_target = forms.IntegerField(
        min_value=5,
        max_value=100,
        initial=20,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'هدف بهبود فروش (%)'})
    )
    
    optimization_timeline = forms.IntegerField(
        min_value=1,
        max_value=24,
        initial=6,
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
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='دقت پیش‌بینی مورد انتظار'
    )
    
    # Final Report
    analyst_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام تحلیلگر'})
    )
    
    report_email = forms.EmailField(
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
