# راهنمای بهینه‌سازی سئو برای هوش مصنوعی‌ها
## AI SEO Optimization Guide for Chidmano

### 🎯 هدف
بهینه‌سازی سایت برای نمایش بهتر در ChatGPT, Perplexity, Claude, Google AI و سایر AI systems.

---

## ✅ کارهای انجام شده

### 1. Allow کردن AI Bots در robots.txt
✅ تمام AI bots مهم مجاز شدند:
- **OpenAI / ChatGPT**: GPTBot, ChatGPT-User, ChatGPTBot
- **Google AI**: Google-Extended
- **Anthropic / Claude**: anthropic-ai, ClaudeBot
- **Perplexity**: PerplexityBot, Perplexity-AI
- **Microsoft AI**: BingPreview
- **Apple AI**: Applebot-Extended
- **Common Crawl**: CCBot (برای AI training)

### 2. AI Bot Detection در Middleware
✅ Middleware برای تشخیص AI bots بهبود یافت:
- `request.is_ai_bot` برای شناسایی AI bots
- Cache headers بهینه برای AI bots (2 hours)
- Header `X-AI-Friendly: true` برای AI bots

### 3. Template Tags برای AI
✅ Template tags جدید:
- `{% ai_friendly_summary %}` - خلاصه AI-friendly
- `{% ai_structured_data %}` - Structured data بهینه
- `{% ai_meta_tags %}` - Meta tags برای AI
- `{% ai_readable_content %}` - محتوای قابل خواندن

### 4. Structured Data بهبود یافته
✅ Enhanced structured data برای AI:
- Description خودکار
- Keywords خودکار
- محتوای غنی‌تر برای AI understanding

---

## 🤖 AI Bots که مجاز هستند

### OpenAI / ChatGPT
```
User-agent: GPTBot
Allow: /
Crawl-delay: 1

User-agent: ChatGPT-User
Allow: /
Crawl-delay: 1

User-agent: ChatGPTBot
Allow: /
Crawl-delay: 1
```

### Google AI
```
User-agent: Google-Extended
Allow: /
Crawl-delay: 1
```

### Anthropic / Claude
```
User-agent: anthropic-ai
Allow: /
Crawl-delay: 1

User-agent: ClaudeBot
Allow: /
Crawl-delay: 1
```

### Perplexity
```
User-agent: PerplexityBot
Allow: /
Crawl-delay: 1

User-agent: Perplexity-AI
Allow: /
Crawl-delay: 1
```

---

## 📋 نکات مهم برای بهینه‌سازی AI SEO

### 1. محتوای متنی واضح
✅ اطمینان حاصل کنید که محتوای اصلی در HTML قابل خواندن است (نه فقط در JavaScript)
✅ استفاده از Semantic HTML (`<article>`, `<section>`, `<header>`, etc.)
✅ استفاده از Heading tags به درستی (H1, H2, H3)

### 2. Structured Data (JSON-LD)
✅ همه صفحات باید Structured Data داشته باشند
✅ استفاده از Schema.org markup
✅ به‌روز نگه داشتن Structured Data

### 3. Meta Tags
✅ Title واضح و توصیفی
✅ Description کامل و اطلاعاتی
✅ استفاده از `{% ai_meta_tags %}`` tag در templates

### 4. محتوای قابل خواندن
✅ حذف محتوای اضافی از HTML
✅ استفاده از `{% ai_readable_content %}` tag
✅ خلاصه‌های واضح با `{% ai_friendly_summary %}`

---

## 🔧 استفاده در Templates

### افزودن AI SEO Tags به Template
```django
{% load ai_seo_tags %}

<!-- در <head> -->
{% ai_structured_data 
    page_type=page_type 
    title=page_title 
    description=page_description 
    url=request.build_absolute_uri 
%}

{% ai_meta_tags %}

<!-- در محتوا -->
<div class="ai-readable-content">
    {% ai_readable_content content %}
</div>

<!-- خلاصه AI-friendly -->
<p class="ai-summary">
    {% ai_friendly_summary content max_length=300 %}
</p>
```

---

## 📊 بررسی عملکرد

### چک کردن robots.txt
```bash
curl https://chidmano.ir/robots.txt | grep -i "gptbot\|claude\|perplexity"
```

### تست AI Bot Detection
```python
from chidmano.ai_seo_optimizer import AIBotDetector

# تست
user_agent = "GPTBot/1.0 (+https://openai.com/gptbot)"
is_ai = AIBotDetector.is_ai_bot(user_agent)
print(f"Is AI Bot: {is_ai}")  # True
```

---

## 🎯 انتظارات

### هفته اول تا دوم:
- AI bots شروع به crawl کردن سایت می‌کنند
- محتوا در سیستم‌های AI ثبت می‌شود

### ماه اول:
- سایت در ChatGPT و Perplexity قابل مشاهده می‌شود
- پاسخ‌های AI دقیق‌تر می‌شوند

### ماه دوم تا سوم:
- بهبود قابل توجه در AI responses
- افزایش ارجاعات به سایت از AI systems

---

## ⚠️ نکات امنیتی

1. **اطلاعات حساس**: مطمئن شوید اطلاعات حساس در صفحات public نیست
2. **Rate Limiting**: AI bots می‌توانند ترافیک زیادی ایجاد کنند - rate limiting فعال است
3. **Cache**: استفاده از cache برای کاهش load
4. **Monitoring**: رصد کردن ترافیک AI bots

---

## 📝 مثال استفاده

### در `base_seo.html`
```django
{% load ai_seo_tags %}

<head>
    <!-- ... سایر meta tags ... -->
    
    <!-- AI SEO Tags -->
    {% ai_structured_data 
        page_type=page_type 
        title=page_title 
        description=page_description 
    %}
    
    {% ai_meta_tags %}
</head>
```

---

## 🔗 منابع مفید

- [OpenAI GPTBot Info](https://platform.openai.com/docs/gptbot)
- [Google AI Training Data Policy](https://policies.google.com/privacy/generative-ai)
- [Anthropic Claude Bot](https://www.anthropic.com/claude)
- [Perplexity Bot Info](https://www.perplexity.ai/)

---

**تاریخ ایجاد**: 2025-11-02  
**نسخه**: 1.0.0  
**وضعیت**: ✅ فعال و آماده

