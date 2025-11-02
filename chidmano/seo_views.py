"""
Views برای SEO
SEO Views
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from django.template.loader import render_to_string
from django.utils import timezone
from .seo_sitemap import sitemap_generator
from .seo_advanced import seo_manager
from .seo_recovery import seo_recovery_manager
from django.contrib.sitemaps import views as sitemap_views
from django.contrib.sitemaps.views import sitemap as django_sitemap
import xml.etree.ElementTree as ET
import json
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

@require_GET
@cache_page(60 * 60 * 12)  # Cache for 12 hours (به‌روزتر برای احیای سئو)
def sitemap_xml(request):
    """تولید sitemap.xml با Django Sitemap Framework"""
    try:
        from .seo_recovery import (
            EnhancedHomeSitemap,
            EnhancedPagesSitemap,
            GuidePagesSitemap,
            ServicePackageSitemap,
            PublicAnalysesSitemap,
            ImageSitemap,
        )
        
        # تعریف sitemaps برای Django Framework
        sitemaps = {
            'home': EnhancedHomeSitemap(),
            'pages': EnhancedPagesSitemap(),
            'guides': GuidePagesSitemap(),
            'services': ServicePackageSitemap(),
            'analyses': PublicAnalysesSitemap(),
            'images': ImageSitemap(),
        }
        
        # استفاده از Django Sitemap Framework
        response = django_sitemap(
            request,
            sitemaps,
            template_name='sitemap.xml',
            content_type='application/xml'
        )
        
        # اضافه کردن headers برای SEO
        response['Cache-Control'] = 'public, max-age=43200'  # 12 hours
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating sitemap: {e}", exc_info=True)
        # Fallback به روش قدیمی
        try:
            sitemap_urls = sitemap_generator.get_sitemap_urls()
            
            root = ET.Element('urlset')
            root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
            root.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
            
            for url_data in sitemap_urls:
                url_elem = ET.SubElement(root, 'url')
                
                loc_elem = ET.SubElement(url_elem, 'loc')
                loc_elem.text = url_data['loc']
                
                lastmod_elem = ET.SubElement(url_elem, 'lastmod')
                lastmod_elem.text = url_data['lastmod']
                
                changefreq_elem = ET.SubElement(url_elem, 'changefreq')
                changefreq_elem.text = url_data['changefreq']
                
                priority_elem = ET.SubElement(url_elem, 'priority')
                priority_elem.text = str(url_data['priority'])
            
            xml_str = ET.tostring(root, encoding='unicode', method='xml')
            response = HttpResponse(xml_str, content_type='application/xml')
            response['Cache-Control'] = 'public, max-age=43200'
            return response
        except Exception as e2:
            logger.error(f"Fallback sitemap generation also failed: {e2}")
            return HttpResponse("Error generating sitemap", status=500)

@require_GET
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def sitemap_index(request):
    """تولید sitemap index"""
    try:
        sitemap_index_data = sitemap_generator.generate_sitemap_index()
        
        # Create XML sitemap index
        root = ET.Element('sitemapindex')
        root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        for sitemap_data in sitemap_index_data['sitemaps']:
            sitemap_elem = ET.SubElement(root, 'sitemap')
            
            loc_elem = ET.SubElement(sitemap_elem, 'loc')
            loc_elem.text = sitemap_data['loc']
            
            lastmod_elem = ET.SubElement(sitemap_elem, 'lastmod')
            lastmod_elem.text = sitemap_data['lastmod']
        
        xml_str = ET.tostring(root, encoding='unicode', method='xml')
        
        response = HttpResponse(xml_str, content_type='application/xml')
        return response
        
    except Exception as e:
        logger.error(f"Error generating sitemap index: {e}")
        return HttpResponse("Error generating sitemap index", status=500)

@require_GET
@cache_page(60 * 60 * 12)  # Cache for 12 hours (کمتر برای به‌روزرسانی سریع‌تر)
def robots_txt(request):
    """تولید robots.txt بهینه برای احیای سئو"""
    try:
        # استفاده از سیستم احیای سئو با پشتیبانی از AI bots
        robots_content = seo_recovery_manager.generate_robots_txt(allow_ai_bots=True)
        response = HttpResponse(robots_content, content_type='text/plain; charset=utf-8')
        # اضافه کردن cache headers برای bots
        response['Cache-Control'] = 'public, max-age=43200'  # 12 hours
        return response
    except Exception as e:
        logger.error(f"Error generating robots.txt: {e}")
        return HttpResponse("Error generating robots.txt", status=500)

@require_GET
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def sitemap_images(request):
    """تولید sitemap برای تصاویر با lastmod به‌روز"""
    try:
        from .seo_recovery import ImageSitemap
        image_sitemap = ImageSitemap()
        
        root = ET.Element('urlset')
        root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        root.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
        
        for item in image_sitemap.items():
            url_elem = ET.SubElement(root, 'url')
            
            loc_elem = ET.SubElement(url_elem, 'loc')
            loc_elem.text = f"https://chidmano.ir{item['url']}"
            
            lastmod_elem = ET.SubElement(url_elem, 'lastmod')
            # استفاده از lastmod از sitemap
            lastmod_date = image_sitemap.lastmod(item)
            if isinstance(lastmod_date, (datetime, date)):
                if isinstance(lastmod_date, datetime):
                    lastmod_elem.text = lastmod_date.strftime('%Y-%m-%d')
                else:
                    lastmod_elem.text = lastmod_date.strftime('%Y-%m-%d')
            else:
                lastmod_elem.text = timezone.now().strftime('%Y-%m-%d')
            
            changefreq_elem = ET.SubElement(url_elem, 'changefreq')
            changefreq_elem.text = image_sitemap.changefreq
            
            priority_elem = ET.SubElement(url_elem, 'priority')
            priority_elem.text = str(image_sitemap.priority)
            
            # Image data
            image_elem = ET.SubElement(url_elem, 'image:image')
            
            image_loc = ET.SubElement(image_elem, 'image:loc')
            image_loc.text = f"https://chidmano.ir{item['url']}"
            
            image_title = ET.SubElement(image_elem, 'image:title')
            image_title.text = item['title']
            
            image_caption = ET.SubElement(image_elem, 'image:caption')
            image_caption.text = item['caption']
            
            # Geo location اگر موجود باشد
            if 'geo_location' in item:
                image_geo = ET.SubElement(image_elem, 'image:geo_location')
                image_geo.text = item['geo_location']
        
        xml_str = ET.tostring(root, encoding='unicode', method='xml')
        
        response = HttpResponse(xml_str, content_type='application/xml')
        response['Cache-Control'] = 'public, max-age=86400'  # 24 hours
        return response
        
    except Exception as e:
        logger.error(f"Error generating image sitemap: {e}", exc_info=True)
        return HttpResponse("Error generating image sitemap", status=500)

@require_GET
def seo_analysis(request, analysis_id):
    """صفحه SEO برای تحلیل خاص"""
    try:
        from store_analysis.models import StoreAnalysis
        analysis = StoreAnalysis.objects.get(pk=analysis_id)
        
        # Generate SEO data
        seo_data = seo_manager.generate_meta_tags(
            page_type='analysis',
            store_name=analysis.store_name,
            analysis_id=analysis_id
        )
        
        structured_data = seo_manager.generate_structured_data(
            page_type='analysis',
            store_name=analysis.store_name,
            analysis_id=analysis_id
        )
        
        context = {
            'analysis': analysis,
            'seo_data': seo_data,
            'structured_data': structured_data,
            'page_type': 'analysis',
            'page_title': seo_data['title'],
            'page_description': seo_data['description'],
            'page_keywords': seo_data['keywords'],
            'og_image': seo_data['og_image'],
            'twitter_image': seo_data.get('twitter_image', seo_data['og_image']),
            'breadcrumbs': [
                {'name': 'خانه', 'url': '/'},
                {'name': 'تحلیل فروشگاه', 'url': '/store/analysis/'},
                {'name': f'تحلیل {analysis.store_name}', 'url': f'/store/analysis/{analysis_id}/results/'}
            ]
        }
        
        return render(request, 'chidmano/seo_analysis.html', context)
        
    except StoreAnalysis.DoesNotExist:
        return HttpResponse("Analysis not found", status=404)
    except Exception as e:
        logger.error(f"Error in seo_analysis view: {e}")
        return HttpResponse("Error loading analysis", status=500)

@require_GET
def seo_home(request):
    """صفحه SEO برای صفحه اصلی"""
    try:
        seo_data = seo_manager.generate_meta_tags(page_type='home')
        structured_data = seo_manager.generate_structured_data(page_type='home')
        
        context = {
            'seo_data': seo_data,
            'structured_data': structured_data,
            'page_type': 'home',
            'page_title': seo_data['title'],
            'page_description': seo_data['description'],
            'page_keywords': seo_data['keywords'],
            'og_image': seo_data['og_image'],
            'twitter_image': seo_data.get('twitter_image', seo_data['og_image']),
        }
        
        return render(request, 'chidmano/seo_home.html', context)
        
    except Exception as e:
        logger.error(f"Error in seo_home view: {e}")
        return HttpResponse("Error loading home page", status=500)

@require_GET
def seo_features(request):
    """صفحه SEO برای ویژگی‌ها"""
    try:
        seo_data = seo_manager.generate_meta_tags(page_type='features')
        structured_data = seo_manager.generate_structured_data(page_type='features')
        
        context = {
            'seo_data': seo_data,
            'structured_data': structured_data,
            'page_type': 'features',
            'page_title': seo_data['title'],
            'page_description': seo_data['description'],
            'page_keywords': seo_data['keywords'],
            'og_image': seo_data['og_image'],
            'twitter_image': seo_data.get('twitter_image', seo_data['og_image']),
            'breadcrumbs': [
                {'name': 'خانه', 'url': '/'},
                {'name': 'ویژگی‌ها', 'url': '/store/features/'}
            ]
        }
        
        return render(request, 'chidmano/seo_features.html', context)
        
    except Exception as e:
        logger.error(f"Error in seo_features view: {e}")
        return HttpResponse("Error loading features page", status=500)

@require_GET
def seo_analytics_dashboard(request):
    """داشبورد آنالیتیکس SEO"""
    if not request.user.is_staff:
        return HttpResponse("Access denied", status=403)
    
    try:
        from .seo_recovery import seo_recovery_manager
        
        # دریافت آمار احیای سئو
        recovery_stats = seo_recovery_manager.get_recovery_stats()
        
        context = {
            'page_title': 'داشبورد آنالیتیکس SEO',
            'recovery_stats': recovery_stats,
            'analytics_data': {
                'total_pages': recovery_stats.get('total_pages_in_sitemap', 0),
                'indexed_pages': 0,
                'backlinks': 0,
                'organic_traffic': 0,
                'recovery_date': recovery_stats.get('recovery_date'),
                'downtime_days': recovery_stats.get('downtime_days', 10),
            }
        }
        
        return render(request, 'chidmano/seo_analytics.html', context)
        
    except Exception as e:
        logger.error(f"Error in seo_analytics_dashboard: {e}", exc_info=True)
        return HttpResponse("Error loading analytics", status=500)


@require_GET
def seo_submit_to_google(request):
    """ارسال sitemap و صفحات مهم به Google Search Console"""
    if not request.user.is_staff:
        return HttpResponse("Access denied", status=403)
    
    try:
        from .seo_google_submit import google_submitter
        
        # ارسال sitemap
        sitemap_result = google_submitter.submit_sitemap()
        
        # ارسال صفحات مهم
        pages_result = google_submitter.submit_important_pages()
        
        context = {
            'sitemap_result': sitemap_result,
            'pages_result': pages_result,
            'total_submitted': len(pages_result.get('successful', [])),
            'total_failed': len(pages_result.get('failed', [])),
        }
        
        return render(request, 'chidmano/seo_submit_result.html', context)
        
    except Exception as e:
        logger.error(f"Error in seo_submit_to_google: {e}", exc_info=True)
        return HttpResponse(f"Error submitting to Google: {str(e)}", status=500)