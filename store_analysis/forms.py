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

# --- فرم تحلیل هوشمند فروشگاه ۷ گامه ---
class AIStoreAnalysisForm(forms.Form):
    """فرم تحلیل هوشمند فروشگاه - ۷ گام بهینه‌سازی"""
    
    # ===== گام 1: اطلاعات پایه فروشگاه (📦 pandas / numpy) =====
    store_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'نام فروشگاه',
            'data-step': '1',
            'data-tooltip': 'این اطلاعات به ما کمک می‌کنه تا ساختار کلی فروشگاه رو بسازیم'
        })
    )
    
    store_type = forms.ChoiceField(
        choices=[
            ('supermarket', 'سوپرمارکت'),
            ('hypermarket', 'هایپرمارکت'),
            ('convenience', 'فروشگاه راحتی'),
            ('clothing', 'فروشگاه پوشاک'),
            ('electronics', 'فروشگاه لوازم الکترونیکی'),
            ('home_appliances', 'فروشگاه لوازم خانگی'),
            ('pharmacy', 'داروخانه'),
            ('bookstore', 'کتابفروشی'),
            ('jewelry', 'فروشگاه جواهرات'),
            ('sports', 'فروشگاه ورزشی'),
            ('cosmetics', 'فروشگاه لوازم آرایشی'),
            ('other', 'سایر'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'data-step': '1',
            'data-tooltip': 'نوع فروشگاه بر الگوی چیدمان تأثیر مستقیم دارد'
        })
    )
    
    store_size = forms.IntegerField(
        min_value=50,
        max_value=10000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'مساحت کل فروشگاه (متر مربع)',
            'data-step': '1',
            'data-tooltip': 'مساحت کل برای محاسبه تراکم و بهینه‌سازی فضا'
        })
    )
    
    # بخش‌های مختلف فروشگاه
    food_section_size = forms.IntegerField(
        min_value=0,
        max_value=5000,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'مساحت بخش مواد غذایی (متر مربع)',
            'data-step': '1'
        })
    )
    
    beverage_section_size = forms.IntegerField(
        min_value=0,
        max_value=2000,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'مساحت بخش نوشیدنی‌ها (متر مربع)',
            'data-step': '1'
        })
    )
    
    household_section_size = forms.IntegerField(
        min_value=0,
        max_value=3000,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'مساحت بخش لوازم خانگی (متر مربع)',
            'data-step': '1'
        })
    )
    
    shelf_count = forms.IntegerField(
        min_value=1,
        max_value=1000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'تعداد کل قفسه‌ها',
            'data-step': '1',
            'data-tooltip': 'تعداد قفسه‌ها برای محاسبه تراکم محصولات'
        })
    )
    
    # ===== گام 2: اطلاعات مشتریان (👥 scikit-learn / scipy) =====
    daily_customers = forms.IntegerField(
        min_value=1,
        max_value=10000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'میانگین مشتریان روزانه',
            'data-step': '2',
            'data-tooltip': 'الگوهای رفتاری مشتریان به ما کمک می‌کنه پیش‌بینی کنیم'
        })
    )
    
    peak_hours = forms.MultipleChoiceField(
        choices=[
            ('morning', 'صبح (8-12)'),
            ('afternoon', 'ظهر (12-16)'),
            ('evening', 'عصر (16-20)'),
            ('night', 'شب (20-24)'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
            'data-step': '2'
        })
    )
    
    purchase_pattern = forms.ChoiceField(
        choices=[
            ('quick', 'خرید سریع (کمتر از 10 دقیقه)'),
            ('medium', 'خرید متوسط (10-30 دقیقه)'),
            ('long', 'خرید طولانی (بیش از 30 دقیقه)'),
            ('mixed', 'ترکیبی از انواع خرید'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'data-step': '2',
            'data-tooltip': 'نوع خرید بر مسیر حرکت مشتریان تأثیر دارد'
        })
    )
    
    repeat_customers_percentage = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'درصد مشتریان تکراری',
            'data-step': '2',
            'data-tooltip': 'مشتریان تکراری الگوی حرکت متفاوتی دارند'
        })
    )
    
    # ===== گام 3: جریان حرکتی مشتریان (➡ networkx) =====
    entrance_to_first_stop = forms.ChoiceField(
        choices=[
            ('immediate', 'بلافاصله (کمتر از 1 دقیقه)'),
            ('short', 'کوتاه (1-3 دقیقه)'),
            ('medium', 'متوسط (3-5 دقیقه)'),
            ('long', 'طولانی (بیش از 5 دقیقه)'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'data-step': '3',
            'data-tooltip': 'با این داده‌ها می‌تونیم شبکه حرکت مشتریان رو شبیه‌سازی کنیم'
        })
    )
    
    high_traffic_areas = forms.MultipleChoiceField(
        choices=[
            ('entrance', 'ورودی فروشگاه'),
            ('checkout', 'صندوق پرداخت'),
            ('promotions', 'بخش تخفیف‌ها'),
            ('essentials', 'مواد ضروری'),
            ('fresh_food', 'مواد غذایی تازه'),
            ('beverages', 'نوشیدنی‌ها'),
            ('snacks', 'تنقلات'),
            ('household', 'لوازم خانگی'),
            ('personal_care', 'لوازم بهداشتی'),
            ('other', 'سایر'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
            'data-step': '3'
        })
    )
    
    ignored_sections = forms.MultipleChoiceField(
        choices=[
            ('electronics', 'لوازم الکترونیکی'),
            ('clothing', 'پوشاک'),
            ('books', 'کتاب‌ها'),
            ('sports', 'لوازم ورزشی'),
            ('jewelry', 'جواهرات'),
            ('cosmetics', 'لوازم آرایشی'),
            ('automotive', 'لوازم خودرو'),
            ('gardening', 'لوازم باغبانی'),
            ('other', 'سایر'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
            'data-step': '3'
        })
    )
    
    # ===== گام 4: تحلیل محصولات و قفسه‌ها (📊 pandas / seaborn) =====
    top_selling_products = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'محصولات پرفروش (مثال: نان، شیر، تخم مرغ، برنج)',
            'data-step': '4',
            'data-tooltip': 'شناخت محصولات مکمل به ما کمک می‌کنه پیشنهادهای چیدمانی بدیم'
        })
    )
    
    complementary_products = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'محصولات مکمل (مثال: نان و پنیر، چای و قند)',
            'data-step': '4'
        })
    )
    
    seasonal_products = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'محصولات فصلی (مثال: میوه‌های تابستانی، لوازم مدرسه)',
            'data-step': '4'
        })
    )
    
    low_selling_products = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'محصولات کم‌فروش',
            'data-step': '4'
        })
    )
    
    # ===== گام 5: چیدمان فعلی (🗺 matplotlib) =====
    fixed_shelves = forms.MultipleChoiceField(
        choices=[
            ('entrance', 'قفسه‌های ورودی'),
            ('checkout', 'قفسه‌های صندوق'),
            ('wall_shelves', 'قفسه‌های دیواری'),
            ('island_shelves', 'قفسه‌های جزیره‌ای'),
            ('refrigerated', 'قفسه‌های یخچالی'),
            ('freezer', 'قفسه‌های فریزر'),
            ('other', 'سایر'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
            'data-step': '5',
            'data-tooltip': 'این بخش کمک می‌کنه بفهمیم چه جاهایی قابل تغییر نیست'
        })
    )
    
    attraction_elements = forms.MultipleChoiceField(
        choices=[
            ('refrigerator', 'یخچال/فریزر'),
            ('promotion_area', 'بخش تخفیف'),
            ('fresh_food_display', 'نمایش مواد تازه'),
            ('beverage_cooler', 'سردکن نوشیدنی'),
            ('bakery', 'نانوایی'),
            ('deli', 'بخش گوشت'),
            ('pharmacy', 'داروخانه'),
            ('atm', 'دستگاه خودپرداز'),
            ('seating_area', 'محل نشستن'),
            ('other', 'سایر'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
            'data-step': '5'
        })
    )
    
    lighting_type = forms.ChoiceField(
        choices=[
            ('natural', 'نور طبیعی'),
            ('fluorescent', 'نور فلورسنت'),
            ('led', 'نور LED'),
            ('halogen', 'نور هالوژن'),
            ('mixed', 'ترکیبی'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'data-step': '5'
        })
    )
    
    # ===== گام 6: اهداف بهینه‌سازی (⚙ scikit-learn) =====
    optimization_goals = forms.MultipleChoiceField(
        choices=[
            ('increase_sales', 'افزایش فروش'),
            ('reduce_congestion', 'کاهش ازدحام'),
            ('improve_experience', 'بهبود تجربه مشتری'),
            ('optimize_space', 'بهینه‌سازی فضا'),
            ('reduce_wait_time', 'کاهش زمان انتظار'),
            ('increase_efficiency', 'افزایش کارایی'),
            ('other', 'سایر'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
            'data-step': '6',
            'data-tooltip': 'این اطلاعات باعث می‌شه تحلیل دقیقاً متناسب با اهداف شما انجام بشه'
        })
    )
    
    priority_goal = forms.ChoiceField(
        choices=[
            ('sales', 'افزایش فروش مهم‌ترین هدف'),
            ('experience', 'بهبود تجربه مشتری مهم‌ترین هدف'),
            ('efficiency', 'افزایش کارایی مهم‌ترین هدف'),
            ('balanced', 'تعادل بین همه اهداف'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'data-step': '6'
        })
    )
    
    budget_constraint = forms.ChoiceField(
        choices=[
            ('low', 'بودجه محدود (کمتر از 10 میلیون تومان)'),
            ('medium', 'بودجه متوسط (10-50 میلیون تومان)'),
            ('high', 'بودجه بالا (بیش از 50 میلیون تومان)'),
            ('unlimited', 'بدون محدودیت بودجه'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'data-step': '6'
        })
    )
    
    # ===== گام 7: خروجی نهایی (📑 UX/Report) =====
    report_detail_level = forms.ChoiceField(
        choices=[
            ('executive', 'خلاصه مدیریتی'),
            ('detailed', 'تحلیل فنی کامل'),
            ('both', 'هر دو نوع گزارش'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'data-step': '7',
            'data-tooltip': 'اینجا مشخص می‌کنید گزارش نهایی دقیقاً چطور باید ارائه بشه'
        })
    )
    
    output_format = forms.MultipleChoiceField(
        choices=[
            ('pdf', 'فایل PDF'),
            ('excel', 'فایل Excel'),
            ('dashboard', 'داشبورد آنلاین'),
            ('presentation', 'ارائه پاورپوینت'),
            ('web_report', 'گزارش وب'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
            'data-step': '7'
        })
    )
    
    include_visualizations = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'data-step': '7'
        })
    )
    
    include_recommendations = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'data-step': '7'
        })
    )
    
    # اطلاعات تماس
    contact_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'نام و نام خانوادگی'
        })
    )
    
    contact_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'ایمیل'
        })
    )
    
    contact_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'شماره تماس'
        })
    )
    
    # فایل‌های آپلود
    store_photos = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    
    store_plan = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.png'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        # اعتبارسنجی مساحت‌ها
        store_size = cleaned_data.get('store_size', 0)
        food_size = cleaned_data.get('food_section_size', 0)
        beverage_size = cleaned_data.get('beverage_section_size', 0)
        household_size = cleaned_data.get('household_section_size', 0)
        
        total_sections = food_size + beverage_size + household_size
        if total_sections > store_size:
            raise ValidationError('مجموع مساحت بخش‌ها نمی‌تواند بیشتر از مساحت کل فروشگاه باشد.')
        
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
