"""
Forms for Store Analysis
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PaymentForm(forms.Form):
    """
    Payment form for customer information
    """
    
    customer_name = forms.CharField(
        max_length=100,
        label='نام و نام خانوادگی',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی خود را وارد کنید',
            'required': True
        })
    )
    
    customer_email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید',
            'required': True
        })
    )
    
    customer_phone = forms.CharField(
        max_length=20,
        label='شماره تلفن',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره تلفن خود را وارد کنید',
            'required': True
        })
    )
    
    def clean_customer_phone(self):
        phone = self.cleaned_data.get('customer_phone')
        if phone:
            # Remove any non-digit characters
            phone = ''.join(filter(str.isdigit, phone))
            if len(phone) < 10:
                raise forms.ValidationError('شماره تلفن باید حداقل 10 رقم باشد')
        return phone
    
    def clean_customer_email(self):
        email = self.cleaned_data.get('customer_email')
        if email:
            # Basic email validation
            if '@' not in email or '.' not in email:
                raise forms.ValidationError('ایمیل معتبر نیست')
        return email


class StoreAnalysisForm(forms.Form):
    """
    Store analysis form
    """
    
    STORE_TYPE_CHOICES = [
        ('supermarket', 'سوپرمارکت'),
        ('grocery', 'خواربار فروشی'),
        ('convenience', 'فروشگاه رفاه'),
        ('pharmacy', 'داروخانه'),
        ('electronics', 'فروشگاه لوازم الکترونیکی'),
        ('clothing', 'فروشگاه پوشاک'),
        ('other', 'سایر'),
    ]
    
    STORE_SIZE_CHOICES = [
        ('small', 'کوچک (کمتر از 50 متر مربع)'),
        ('medium', 'متوسط (50-200 متر مربع)'),
        ('large', 'بزرگ (200-500 متر مربع)'),
        ('xlarge', 'خیلی بزرگ (بیش از 500 متر مربع)'),
    ]
    
    store_name = forms.CharField(
        max_length=200,
        label='نام فروشگاه',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام فروشگاه خود را وارد کنید',
            'required': True
        })
    )
    
    store_type = forms.ChoiceField(
        choices=STORE_TYPE_CHOICES,
        label='نوع فروشگاه',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    store_size = forms.ChoiceField(
        choices=STORE_SIZE_CHOICES,
        label='اندازه فروشگاه',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    store_address = forms.CharField(
        max_length=500,
        label='آدرس فروشگاه',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'آدرس کامل فروشگاه خود را وارد کنید',
            'rows': 3,
            'required': True
        })
    )
    
    store_description = forms.CharField(
        max_length=1000,
        label='توضیحات فروشگاه',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'توضیحات بیشتری درباره فروشگاه خود ارائه دهید',
            'rows': 4,
            'required': False
        })
    )
    
    contact_name = forms.CharField(
        max_length=100,
        label='نام مسئول',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام مسئول فروشگاه',
            'required': True
        })
    )
    
    contact_phone = forms.CharField(
        max_length=20,
        label='شماره تماس',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره تماس مسئول',
            'required': True
        })
    )
    
    contact_email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل مسئول',
            'required': True
        })
    )
    
    def clean_contact_phone(self):
        phone = self.cleaned_data.get('contact_phone')
        if phone:
            # Remove any non-digit characters
            phone = ''.join(filter(str.isdigit, phone))
            if len(phone) < 10:
                raise forms.ValidationError('شماره تلفن باید حداقل 10 رقم باشد')
        return phone
    
    def clean_contact_email(self):
        email = self.cleaned_data.get('contact_email')
        if email:
            # Basic email validation
            if '@' not in email or '.' not in email:
                raise forms.ValidationError('ایمیل معتبر نیست')
        return email


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form with additional fields
    """
    
    email = forms.EmailField(
        required=True,
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='نام',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خود را وارد کنید'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خانوادگی خود را وارد کنید'
        })
    )
    
    phone = forms.CharField(
        max_length=11,
        required=True,
        label='شماره موبایل',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '09123456789',
            'pattern': '09[0-9]{9}',
            'title': 'شماره موبایل باید با 09 شروع شود و 11 رقم باشد'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری خود را وارد کنید'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'رمز عبور را مجدداً وارد کنید'
        })
        
        # اصلاح validation برای username
        self.fields['username'].validators = []
    
    def clean_phone(self):
        """اعتبارسنجی شماره موبایل"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # حذف فاصله‌ها و خط تیره
            phone = phone.replace(' ', '').replace('-', '')
            
            # بررسی طول
            if len(phone) != 11:
                raise forms.ValidationError('شماره موبایل باید 11 رقم باشد')
            
            # بررسی شروع با 09
            if not phone.startswith('09'):
                raise forms.ValidationError('شماره موبایل باید با 09 شروع شود')
            
            # بررسی عددی بودن
            if not phone.isdigit():
                raise forms.ValidationError('شماره موبایل باید فقط شامل اعداد باشد')
            
            # بررسی تکراری نبودن
            from store_analysis.models import UserProfile
            if UserProfile.objects.filter(phone=phone).exists():
                raise forms.ValidationError('این شماره موبایل قبلاً ثبت شده است')
        
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلاً ثبت شده است')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # ایجاد UserProfile ساده (safe برای فیلدهای missing)
            try:
                from .utils.safe_db import safe_create_userprofile
                safe_create_userprofile(user, self.cleaned_data['phone'])
            except Exception as e:
                # اگر UserProfile ایجاد نشد، لاگ کن اما کاربر را ایجاد کن
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error creating UserProfile for user {user.username}: {e}")
        return user
