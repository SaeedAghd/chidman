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
import xml.etree.ElementTree as ET
import json
import logging

logger = logging.getLogger(__name__)

@require_GET
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def sitemap_xml(request):
    """تولید sitemap.xml"""
    try:
        sitemap_urls = sitemap_generator.get_sitemap_urls()
        
        # Create XML sitemap
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
        
        # Convert to string
        xml_str = ET.tostring(root, encoding='unicode', method='xml')
        
        response = HttpResponse(xml_str, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="sitemap.xml"'
        return response
        
    except Exception as e:
        logger.error(f"Error generating sitemap: {e}")
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
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def robots_txt(request):
    """تولید robots.txt"""
    try:
        robots_content = sitemap_generator.generate_robots_txt()
        response = HttpResponse(robots_content, content_type='text/plain')
        return response
    except Exception as e:
        logger.error(f"Error generating robots.txt: {e}")
        return HttpResponse("Error generating robots.txt", status=500)

@require_GET
def sitemap_images(request):
    """تولید sitemap برای تصاویر"""
    try:
        from .seo_sitemap import ImageSitemap
        image_sitemap = ImageSitemap()
        
        root = ET.Element('urlset')
        root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        root.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
        
        for item in image_sitemap.items():
            url_elem = ET.SubElement(root, 'url')
            
            loc_elem = ET.SubElement(url_elem, 'loc')
            loc_elem.text = f"https://chidmano.ir{item['url']}"
            
            lastmod_elem = ET.SubElement(url_elem, 'lastmod')
            lastmod_elem.text = timezone.now().strftime('%Y-%m-%d')
            
            # Image data
            image_elem = ET.SubElement(url_elem, 'image:image')
            
            image_loc = ET.SubElement(image_elem, 'image:loc')
            image_loc.text = f"https://chidmano.ir{item['url']}"
            
            image_title = ET.SubElement(image_elem, 'image:title')
            image_title.text = item['title']
            
            image_caption = ET.SubElement(image_elem, 'image:caption')
            image_caption.text = item['caption']
        
        xml_str = ET.tostring(root, encoding='unicode', method='xml')
        
        response = HttpResponse(xml_str, content_type='application/xml')
        return response
        
    except Exception as e:
        logger.error(f"Error generating image sitemap: {e}")
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
        # در آینده می‌توان آمار SEO را از Google Analytics دریافت کرد
        context = {
            'page_title': 'داشبورد آنالیتیکس SEO',
            'analytics_data': {
                'total_pages': 0,
                'indexed_pages': 0,
                'backlinks': 0,
                'organic_traffic': 0
            }
        }
        
        return render(request, 'chidmano/seo_analytics.html', context)
        
    except Exception as e:
        logger.error(f"Error in seo_analytics_dashboard: {e}")
        return HttpResponse("Error loading analytics", status=500)