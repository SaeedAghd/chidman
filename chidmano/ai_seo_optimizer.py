#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سیستم بهینه‌سازی سئو برای هوش مصنوعی‌ها
AI SEO Optimization System for ChatGPT, Perplexity, Claude, etc.
"""

import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


class AIBotDetector:
    """تشخیص و مدیریت AI bots"""
    
    # لیست AI bots مهم
    AI_BOTS = {
        # OpenAI / ChatGPT
        'ChatGPT-User': {
            'name': 'ChatGPT',
            'description': 'OpenAI ChatGPT Browser',
            'allow': True,
            'crawl_delay': 1,
        },
        'GPTBot': {
            'name': 'OpenAI GPTBot',
            'description': 'OpenAI GPTBot Crawler',
            'allow': True,
            'crawl_delay': 1,
        },
        'ChatGPTBot': {
            'name': 'ChatGPT Bot',
            'description': 'ChatGPT Web Crawler',
            'allow': True,
            'crawl_delay': 1,
        },
        
        # Google AI
        'Google-Extended': {
            'name': 'Google Extended',
            'description': 'Google AI Training Data Crawler',
            'allow': True,
            'crawl_delay': 1,
        },
        'GoogleOther': {
            'name': 'Google AI',
            'description': 'Google AI Systems',
            'allow': True,
            'crawl_delay': 1,
        },
        
        # Anthropic / Claude
        'anthropic-ai': {
            'name': 'Anthropic Claude',
            'description': 'Anthropic Claude AI',
            'allow': True,
            'crawl_delay': 1,
        },
        'ClaudeBot': {
            'name': 'Claude Bot',
            'description': 'Anthropic Claude Web Crawler',
            'allow': True,
            'crawl_delay': 1,
        },
        
        # Perplexity
        'PerplexityBot': {
            'name': 'Perplexity',
            'description': 'Perplexity AI Search',
            'allow': True,
            'crawl_delay': 1,
        },
        'Perplexity-AI': {
            'name': 'Perplexity AI',
            'description': 'Perplexity AI Crawler',
            'allow': True,
            'crawl_delay': 1,
        },
        
        # Microsoft AI
        'BingPreview': {
            'name': 'Bing AI',
            'description': 'Microsoft Bing AI',
            'allow': True,
            'crawl_delay': 1,
        },
        'MSNBot': {
            'name': 'Microsoft Bot',
            'description': 'Microsoft AI Systems',
            'allow': True,
            'crawl_delay': 1,
        },
        
        # سایر AI Systems
        'CCBot': {
            'name': 'Common Crawl',
            'description': 'Common Crawl AI Training',
            'allow': True,
            'crawl_delay': 2,
        },
        'anthropic': {
            'name': 'Anthropic',
            'description': 'Anthropic AI',
            'allow': True,
            'crawl_delay': 1,
        },
        'Applebot-Extended': {
            'name': 'Apple AI',
            'description': 'Apple AI Systems',
            'allow': True,
            'crawl_delay': 1,
        },
    }
    
    @classmethod
    def is_ai_bot(cls, user_agent):
        """تشخیص AI bot از user agent"""
        if not user_agent:
            return False
        
        user_agent_lower = user_agent.lower()
        
        for bot_id, bot_info in cls.AI_BOTS.items():
            if bot_id.lower() in user_agent_lower:
                return True
        
        # همچنین بررسی patterns عمومی
        ai_patterns = [
            'gptbot',
            'chatgpt',
            'claude',
            'anthropic',
            'perplexity',
            'ai-agent',
            'ai-crawler',
            'ai-bot',
        ]
        
        return any(pattern in user_agent_lower for pattern in ai_patterns)
    
    @classmethod
    def get_ai_bot_info(cls, user_agent):
        """دریافت اطلاعات AI bot"""
        if not user_agent:
            return None
        
        user_agent_lower = user_agent.lower()
        
        for bot_id, bot_info in cls.AI_BOTS.items():
            if bot_id.lower() in user_agent_lower:
                return bot_info
        
        return None
    
    @classmethod
    def should_allow_ai_bot(cls, user_agent):
        """بررسی اینکه آیا AI bot مجاز است یا نه"""
        bot_info = cls.get_ai_bot_info(user_agent)
        if bot_info:
            return bot_info.get('allow', True)
        return True  # به صورت پیش‌فرض allow می‌کنیم


class AISEOOptimizer:
    """بهینه‌سازی محتوا برای AI"""
    
    @staticmethod
    def generate_ai_friendly_summary(content, max_length=500):
        """تولید خلاصه AI-friendly از محتوا"""
        # حذف HTML tags
        import re
        clean_content = re.sub(r'<[^>]+>', '', content)
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
        
        # محدود کردن طول
        if len(clean_content) > max_length:
            clean_content = clean_content[:max_length] + '...'
        
        return clean_content
    
    @staticmethod
    def enhance_structured_data_for_ai(structured_data):
        """بهبود structured data برای AI"""
        # اضافه کردن اطلاعات بیشتر برای AI
        if isinstance(structured_data, dict):
            enhanced = structured_data.copy()
            
            # اضافه کردن description اگر وجود ندارد
            if '@type' in enhanced and 'description' not in enhanced:
                enhanced['description'] = enhanced.get('name', '') + ' - ' + enhanced.get('headline', '')
            
            # اضافه کردن keywords اگر وجود ندارد
            if 'keywords' not in enhanced:
                keywords = []
                if enhanced.get('name'):
                    keywords.append(enhanced['name'])
                if enhanced.get('headline'):
                    keywords.append(enhanced['headline'])
                if keywords:
                    enhanced['keywords'] = ', '.join(keywords)
            
            return enhanced
        
        return structured_data
    
    @staticmethod
    def generate_ai_readable_content(page_data):
        """تولید محتوای قابل خواندن برای AI"""
        ai_content = {
            'title': page_data.get('title', ''),
            'description': page_data.get('description', ''),
            'summary': AISEOOptimizer.generate_ai_friendly_summary(
                page_data.get('content', ''),
                max_length=300
            ),
            'key_points': page_data.get('key_points', []),
            'faq': page_data.get('faq', []),
            'structured_data': AISEOOptimizer.enhance_structured_data_for_ai(
                page_data.get('structured_data', {})
            ),
        }
        
        return ai_content


class AIRobotsTxtGenerator:
    """تولید robots.txt با پشتیبانی از AI bots"""
    
    @staticmethod
    def generate_ai_friendly_robots_txt(base_robots_content, allow_ai=True):
        """تولید robots.txt با تنظیمات AI-friendly"""
        
        if not allow_ai:
            # اگر نمی‌خواهیم AI bots را allow کنیم
            ai_section = """
# ===== AI Bots - مسدود شده =====
User-agent: ChatGPT-User
Disallow: /

User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /
"""
            return base_robots_content + ai_section
        
        # بخش AI bots - مجاز
        ai_section = """
# ===== AI Bots - مجاز برای SEO AI =====
# این بخش اجازه می‌دهد AI bots سایت را crawl کنند
# تا در ChatGPT, Perplexity, Claude و سایر AI systems نشان داده شوند

User-agent: GPTBot
Allow: /
Crawl-delay: 1

User-agent: ChatGPT-User
Allow: /
Crawl-delay: 1

User-agent: Google-Extended
Allow: /
Crawl-delay: 1

User-agent: anthropic-ai
Allow: /
Crawl-delay: 1

User-agent: ClaudeBot
Allow: /
Crawl-delay: 1

User-agent: PerplexityBot
Allow: /
Crawl-delay: 1

User-agent: Perplexity-AI
Allow: /
Crawl-delay: 1

User-agent: CCBot
Allow: /
Crawl-delay: 2

User-agent: Applebot-Extended
Allow: /
Crawl-delay: 1

User-agent: BingPreview
Allow: /
Crawl-delay: 1

# ===== AI Training Data - مجاز =====
# این bots برای آموزش AI models استفاده می‌شوند
# با allow کردن آنها، محتوای شما در AI responses بهتر نمایش داده می‌شود
"""
        
        # افزودن AI section به robots.txt
        # باید قبل از User-agent: * اضافه شود
        lines = base_robots_content.split('\n')
        
        # پیدا کردن آخرین User-agent section
        ai_section_inserted = False
        result_lines = []
        
        for i, line in enumerate(lines):
            result_lines.append(line)
            
            # بعد از آخرین User-agent: * section، AI section را اضافه کن
            if line.strip() == 'User-agent: *' and i < len(lines) - 1:
                # بررسی خط بعدی
                if lines[i + 1].strip().startswith('Allow:') or lines[i + 1].strip().startswith('Disallow:'):
                    # بعد از این section، AI section را اضافه کن
                    if not ai_section_inserted:
                        result_lines.append(ai_section)
                        ai_section_inserted = True
        
        # اگر AI section اضافه نشد، در انتها اضافه کن
        if not ai_section_inserted:
            result_lines.append(ai_section)
        
        return '\n'.join(result_lines)


# Global instances
ai_bot_detector = AIBotDetector()
ai_seo_optimizer = AISEOOptimizer()
ai_robots_generator = AIRobotsTxtGenerator()

