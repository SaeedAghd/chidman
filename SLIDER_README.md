# اسلایدر پیشرفته چیدمانو

## 📋 **خلاصه**

اسلایدر پیشرفته و کاملاً بازنویسی شده برای صفحه اصلی چیدمانو که مشکل نمایش صفحه سفید در اسلایدهای ۲ و ۳ را حل کرده است.

## 🔧 **مشکلات حل شده**

### 1. **مشکل صفحه سفید**
- **علت**: CSS نادرست و JavaScript قدیمی
- **راه‌حل**: بازنویسی کامل CSS و JavaScript

### 2. **مشکلات عملکرد**
- **علت**: انیمیشن‌های سنگین و عدم بهینه‌سازی
- **راه‌حل**: استفاده از `transform3d` و `will-change`

### 3. **مشکلات دسترسی‌پذیری**
- **علت**: عدم پشتیبانی از ARIA و keyboard navigation
- **راه‌حل**: اضافه کردن ARIA attributes و keyboard support

## 🚀 **ویژگی‌های جدید**

### 1. **عملکرد بهینه**
- استفاده از `transform3d` برای شتاب سخت‌افزاری
- `will-change` برای بهینه‌سازی انیمیشن‌ها
- Lazy loading برای تصاویر
- Debounced resize handling

### 2. **دسترسی‌پذیری کامل**
- ARIA labels و roles
- Keyboard navigation (Arrow keys, Home, End)
- Screen reader support
- Focus management
- High contrast mode support

### 3. **تجربه کاربری پیشرفته**
- Touch/swipe support برای موبایل
- Auto-pause on hover/focus
- Smooth transitions
- Loading states
- Error handling

### 4. **Responsive Design**
- Mobile-first approach
- Touch-friendly controls
- Adaptive sizing
- Reduced motion support

## 📁 **ساختار فایل‌ها**

```
static/
├── css/
│   └── slider.css          # استایل‌های اسلایدر
├── js/
│   ├── slider.js           # کلاس اصلی اسلایدر
│   └── slider-test.js      # تست و دیباگ
└── images/
    └── slider/
        ├── slide1.jpg      # تصویر اسلاید ۱
        ├── slide2.jpg      # تصویر اسلاید ۲
        └── slide3.jpg      # تصویر اسلاید ۳
```

## 🎯 **نحوه استفاده**

### 1. **HTML Structure**
```html
<div class="slider-container" role="region" aria-label="نمونه فروشگاه‌های بهینه شده">
    <div class="slider" role="list">
        <div class="slide" role="listitem" aria-hidden="false">
            <img src="{% static 'images/slider/slide1.jpg' %}" alt="توضیحات تصویر" loading="lazy">
            <div class="slide-content">
                <h3>عنوان اسلاید</h3>
                <p>توضیحات اسلاید</p>
            </div>
        </div>
        <!-- سایر اسلایدها -->
    </div>
    
    <!-- Navigation Dots -->
    <div class="slider-nav" role="tablist" aria-label="انتخاب اسلاید">
        <button class="slider-dot active" role="tab" aria-selected="true"></button>
        <!-- سایر dots -->
    </div>
    
    <!-- Navigation Arrows -->
    <button class="slider-arrow slider-prev" aria-label="اسلاید قبلی">
        <i class="fas fa-chevron-right" aria-hidden="true"></i>
    </button>
    <button class="slider-arrow slider-next" aria-label="اسلاید بعدی">
        <i class="fas fa-chevron-left" aria-hidden="true"></i>
    </button>
</div>
```

### 2. **JavaScript API**
```javascript
// دسترسی به instance اسلایدر
const slider = window.slider;

// تغییر اسلاید
slider.nextSlide();
slider.prevSlide();
slider.goToSlide(2);

// کنترل auto-slide
slider.startAutoSlide();
slider.stopAutoSlide();

// دریافت اطلاعات اسلاید فعلی
const info = slider.getCurrentSlideInfo();
console.log(info); // { index: 0, total: 3, slide: element, isTransitioning: false }

// حذف اسلایدر
slider.destroy();
```

### 3. **Configuration Options**
```javascript
const slider = new AdvancedSlider({
    autoSlide: true,              // auto-slide فعال
    autoSlideInterval: 5000,      // فاصله زمانی (ms)
    transitionDuration: 500,      // مدت انیمیشن (ms)
    pauseOnHover: true,           // توقف روی hover
    pauseOnFocus: true,           // توقف روی focus
    keyboardNavigation: true,     // ناوبری با کیبورد
    touchSupport: true            // پشتیبانی از touch
});
```

## 🧪 **تست و دیباگ**

### 1. **تست خودکار**
در development mode، تست‌های خودکار اجرا می‌شوند:
- تست وجود عناصر HTML
- تست بارگذاری تصاویر
- تست CSS properties
- تست JavaScript functionality
- تست عملکرد اسلایدر

### 2. **Console Debug**
```javascript
// بررسی وضعیت اسلایدر
console.log(window.slider);

// اجرای تست دستی
const tester = new SliderTester();
tester.runAllTests();
```

### 3. **Event Listeners**
```javascript
// گوش دادن به events
document.addEventListener('slider:initialized', (e) => {
    console.log('اسلایدر آماده شد:', e.detail);
});

document.addEventListener('slider:slideChanged', (e) => {
    console.log('اسلاید تغییر کرد:', e.detail);
});

document.addEventListener('slider:imageLoaded', (e) => {
    console.log('تصویر بارگذاری شد:', e.detail);
});

document.addEventListener('slider:imageError', (e) => {
    console.log('خطا در بارگذاری تصویر:', e.detail);
});
```

## 🔧 **عیب‌یابی**

### 1. **مشکل: تصاویر نمایش داده نمی‌شوند**
**راه‌حل:**
- بررسی وجود فایل‌های تصاویر در `static/images/slider/`
- بررسی Django static files configuration
- بررسی Network tab در Developer Tools

### 2. **مشکل: اسلایدر کار نمی‌کند**
**راه‌حل:**
- بررسی Console برای JavaScript errors
- بررسی load شدن فایل‌های CSS و JS
- اجرای تست‌های خودکار

### 3. **مشکل: انیمیشن‌ها کند هستند**
**راه‌حل:**
- بررسی `will-change` و `transform3d`
- بررسی performance در Developer Tools
- فعال کردن hardware acceleration

## 📱 **Responsive Breakpoints**

```css
/* Desktop */
.slider-container { height: 400px; }

/* Tablet */
@media (max-width: 768px) {
    .slider-container { height: 250px; }
}

/* Mobile */
@media (max-width: 480px) {
    .slider-container { height: 200px; }
}
```

## ♿ **دسترسی‌پذیری**

### 1. **ARIA Support**
- `role="region"` برای container
- `role="list"` و `role="listitem"` برای slides
- `role="tablist"` و `role="tab"` برای dots
- `aria-label` برای navigation
- `aria-hidden` برای slides غیرفعال

### 2. **Keyboard Navigation**
- `Arrow Left/Right`: تغییر اسلاید
- `Home/End`: رفتن به اولین/آخرین اسلاید
- `Tab`: ناوبری بین controls
- `Enter/Space`: فعال کردن controls

### 3. **Screen Reader Support**
- ARIA live regions برای announcements
- Descriptive alt texts
- Proper heading structure
- Focus indicators

## 🎨 **Customization**

### 1. **تغییر رنگ‌ها**
```css
:root {
    --slider-primary-color: #2056a7;
    --slider-secondary-color: #00c9a7;
    --slider-overlay-color: rgba(32,86,167,0.8);
}
```

### 2. **تغییر اندازه‌ها**
```css
.slider-container {
    height: 500px; /* تغییر ارتفاع */
}

.slider-arrow {
    width: 60px;   /* تغییر اندازه دکمه‌ها */
    height: 60px;
}
```

### 3. **تغییر انیمیشن‌ها**
```css
.slider {
    transition: transform 0.3s ease-in-out; /* تغییر timing */
}
```

## 📊 **Performance Metrics**

### 1. **Core Web Vitals**
- **LCP**: < 2.5s (با lazy loading)
- **FID**: < 100ms (با optimized event handling)
- **CLS**: < 0.1 (با proper sizing)

### 2. **Optimization Techniques**
- Hardware acceleration با `transform3d`
- Debounced resize events
- Efficient DOM queries
- Minimal reflows/repaints

## 🔄 **Migration Guide**

### از اسلایدر قدیمی:
1. حذف CSS قدیمی اسلایدر
2. حذف JavaScript قدیمی
3. اضافه کردن فایل‌های جدید
4. به‌روزرسانی HTML structure
5. تست عملکرد

## 📝 **Changelog**

### v2.0.0 (Current)
- ✅ بازنویسی کامل CSS و JavaScript
- ✅ حل مشکل صفحه سفید
- ✅ اضافه کردن accessibility features
- ✅ بهبود performance
- ✅ اضافه کردن touch support
- ✅ اضافه کردن test suite

### v1.0.0 (Previous)
- ❌ مشکل صفحه سفید
- ❌ عدم پشتیبانی از accessibility
- ❌ عملکرد ضعیف
- ❌ عدم پشتیبانی از touch

## 🤝 **Contributing**

برای بهبود اسلایدر:
1. Fork کنید
2. Feature branch ایجاد کنید
3. تغییرات را commit کنید
4. Pull request ارسال کنید

## 📄 **License**

این کامپوننت تحت MIT License منتشر شده است.
