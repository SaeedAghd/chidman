#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سیستم ارسال مجدد URL ها به Google Search Console
Google Search Console Re-submission System
"""

import requests
import logging
from django.conf import settings
from django.utils import timezone
from datetime import datetime

logger = logging.getLogger(__name__)


class GoogleSearchConsoleSubmitter:
    """ارسال URL ها به Google Search Console"""
    
    def __init__(self):
        self.api_endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        self.site_url = getattr(settings, 'SITE_URL', 'https://chidmano.ir')
        
        # Google Search Console API credentials (از environment variables)
        self.api_key = getattr(settings, 'GOOGLE_SEARCH_CONSOLE_API_KEY', None)
        self.access_token = getattr(settings, 'GOOGLE_ACCESS_TOKEN', None)
        
        if not self.api_key:
            logger.warning("⚠️ GOOGLE_SEARCH_CONSOLE_API_KEY تنظیم نشده است")
    
    def submit_url(self, url, notification_type='URL_UPDATED'):
        """
        ارسال یک URL به Google Search Console
        
        Args:
            url: URL برای ارسال (relatively یا absolute)
            notification_type: نوع اطلاع‌رسانی ('URL_UPDATED' یا 'URL_DELETED')
        
        Returns:
            dict: نتیجه ارسال
        """
        if not self.access_token:
            logger.warning("⚠️ Google Access Token تنظیم نشده است")
            return {
                'success': False,
                'message': 'Google Access Token تنظیم نشده است'
            }
        
        # تبدیل به absolute URL
        if not url.startswith('http'):
            url = f"{self.site_url}{url}"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            'url': url,
            'type': notification_type,
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"✅ URL successfully submitted to Google: {url}")
                return {
                    'success': True,
                    'url': url,
                    'response': response.json()
                }
            else:
                logger.error(f"❌ Error submitting URL to Google: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'url': url,
                    'status_code': response.status_code,
                    'message': response.text
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error submitting URL to Google: {e}")
            return {
                'success': False,
                'url': url,
                'error': str(e)
            }
    
    def submit_sitemap(self, sitemap_url=None):
        """
        ارسال sitemap به Google Search Console
        
        Note: این کار باید از طریق Google Search Console UI انجام شود
        یا از طریق sitemap submission API
        
        Returns:
            dict: نتیجه ارسال
        """
        if not sitemap_url:
            sitemap_url = f"{self.site_url}/sitemap.xml"
        
        # ارسال sitemap از طریق ping (روش ساده)
        try:
            ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"
            response = requests.get(ping_url, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ Sitemap pinged to Google: {sitemap_url}")
                return {
                    'success': True,
                    'sitemap_url': sitemap_url,
                    'message': 'Sitemap successfully pinged to Google'
                }
            else:
                logger.warning(f"⚠️ Sitemap ping returned status {response.status_code}")
                return {
                    'success': False,
                    'sitemap_url': sitemap_url,
                    'status_code': response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error pinging sitemap to Google: {e}")
            return {
                'success': False,
                'sitemap_url': sitemap_url,
                'error': str(e)
            }
    
    def submit_batch_urls(self, urls, notification_type='URL_UPDATED'):
        """
        ارسال چند URL به صورت batch
        
        Args:
            urls: لیست URL ها
            notification_type: نوع اطلاع‌رسانی
        
        Returns:
            dict: نتایج ارسال
        """
        results = {
            'successful': [],
            'failed': [],
            'total': len(urls)
        }
        
        for url in urls:
            result = self.submit_url(url, notification_type)
            if result.get('success'):
                results['successful'].append(url)
            else:
                results['failed'].append({
                    'url': url,
                    'error': result.get('message', result.get('error', 'Unknown error'))
                })
        
        logger.info(
            f"📊 Batch submission complete: {len(results['successful'])}/{results['total']} successful"
        )
        
        return results
    
    def submit_important_pages(self):
        """
        ارسال صفحات مهم سایت به Google
        
        Returns:
            dict: نتایج ارسال
        """
        important_urls = [
            '/',
            '/store/products/',
            '/store/features/',
            '/store/forms/',
            '/guide/store-layout/',
            '/about/',
        ]
        
        return self.submit_batch_urls(important_urls, 'URL_UPDATED')


class BingWebmasterSubmitter:
    """ارسال URL ها به Bing Webmaster Tools"""
    
    def __init__(self):
        self.site_url = getattr(settings, 'SITE_URL', 'https://chidmano.ir')
        self.api_key = getattr(settings, 'BING_WEBMASTER_API_KEY', None)
        
        if not self.api_key:
            logger.warning("⚠️ BING_WEBMASTER_API_KEY تنظیم نشده است")
    
    def submit_url(self, url):
        """ارسال URL به Bing"""
        # Bing از sitemap ping استفاده می‌کند
        # یا از Bing Webmaster Tools API
        if not url.startswith('http'):
            url = f"{self.site_url}{url}"
        
        try:
            ping_url = f"https://www.bing.com/ping?sitemap={self.site_url}/sitemap.xml"
            response = requests.get(ping_url, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ Sitemap pinged to Bing")
                return {'success': True}
            else:
                return {'success': False, 'status_code': response.status_code}
                
        except Exception as e:
            logger.error(f"❌ Error pinging sitemap to Bing: {e}")
            return {'success': False, 'error': str(e)}


# Global instances
google_submitter = GoogleSearchConsoleSubmitter()
bing_submitter = BingWebmasterSubmitter()

