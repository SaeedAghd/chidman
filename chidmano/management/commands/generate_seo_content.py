from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chidmano.models import BlogPost, SEOKeyword
from chidmano.seo_utils import ContentGenerator, LinkBuilder, KeywordOptimizer
import random

class Command(BaseCommand):
    help = 'تولید محتوای SEO خودکار'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='تعداد مقالات تولید شده'
        )
        parser.add_argument(
            '--keyword',
            type=str,
            help='کلمه کلیدی خاص برای تولید محتوا'
        )

    def handle(self, *args, **options):
        count = options['count']
        specific_keyword = options.get('keyword')
        
        # دریافت نویسنده پیش‌فرض
        author = User.objects.filter(is_staff=True).first()
        if not author:
            self.stdout.write(
                self.style.ERROR('هیچ کاربر ادمین یافت نشد!')
            )
            return
        
        generator = ContentGenerator()
        link_builder = LinkBuilder()
        optimizer = KeywordOptimizer()
        
        generated_count = 0
        
        for i in range(count):
            # انتخاب کلمه کلیدی
            if specific_keyword:
                keyword = specific_keyword
            else:
                keyword = random.choice(generator.keywords)
            
            # تولید محتوا
            content_type = random.choice(['tips', 'comparison', 'case_study'])
            content_data = generator.generate_content(keyword, content_type)
            
            # بهینه‌سازی محتوا
            optimized = optimizer.optimize_content(content_data['content'], keyword)
            
            # اضافه کردن لینک‌های داخلی
            linked_content = link_builder.add_internal_links(optimized['content'])
            
            # ایجاد اسلاگ
            slug = keyword.replace(' ', '-').replace('‌', '-')
            slug = f"{slug}-{i+1}"
            
            # ذخیره در دیتابیس
            blog_post = BlogPost.objects.create(
                title=content_data['title'],
                slug=slug,
                content=linked_content,
                excerpt=content_data['excerpt'],
                author=author,
                published=True,
                meta_description=content_data['meta_description'],
                meta_keywords=content_data['meta_keywords']
            )
            
            # ذخیره کلمه کلیدی
            seo_keyword, created = SEOKeyword.objects.get_or_create(
                keyword=keyword,
                defaults={
                    'search_volume': random.randint(100, 5000),
                    'difficulty': random.randint(20, 80),
                    'cpc': random.uniform(0.5, 5.0),
                    'target_url': f'/blog/{slug}/'
                }
            )
            
            generated_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'مقاله "{content_data["title"]}" ایجاد شد')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'{generated_count} مقاله با موفقیت تولید شد!')
        )
