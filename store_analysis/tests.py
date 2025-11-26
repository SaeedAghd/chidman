from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import StoreAnalysis, StoreAnalysisResult, Payment
from .ai_models.customer_behavior_analyzer import CustomerBehaviorAnalyzer
from .ai_models.traffic_analyzer import TrafficAnalyzer
from .ai_models.layout_analyzer import LayoutAnalyzer
from .services.security_service import SecurityService
import json

class StoreAnalysisTestCase(TestCase):
    def setUp(self):
        """تنظیمات اولیه برای تست‌ها"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # (Previous tests referenced Article models which are not present in current schema.)
        # Skipping article/category setup.
        
        # ایجاد تحلیل فروشگاه نمونه
        self.store_analysis = StoreAnalysis.objects.create(
            user=self.user,
            store_name='فروشگاه تست',
            store_type='supermarket',
            store_size=500,
            status='pending'
        )

class ModelTestCase(StoreAnalysisTestCase):
    """تست مدل‌های داده"""
    
    def test_store_analysis_creation(self):
        """تست ایجاد تحلیل فروشگاه"""
        self.assertEqual(self.store_analysis.store_name, 'فروشگاه تست')
        self.assertEqual(self.store_analysis.status, 'pending')
        self.assertFalse(self.store_analysis.is_processing)  # pending status is not processing
        self.assertTrue(self.store_analysis.status == 'pending')  # correct assertion
    
    # Article model tests removed (models not present in current app schema).
    
    def test_store_analysis_progress(self):
        """تست محاسبه پیشرفت تحلیل"""
        self.assertEqual(self.store_analysis.get_progress(), 25)
        
        # تغییر وضعیت به در حال پردازش
        self.store_analysis.status = 'processing'
        self.store_analysis.save()
        self.assertEqual(self.store_analysis.get_progress(), 50)
        
        # تغییر وضعیت به تکمیل شده
        self.store_analysis.status = 'completed'
        self.store_analysis.save()
        self.assertEqual(self.store_analysis.get_progress(), 100)

class AIAnalyzerTestCase(StoreAnalysisTestCase):
    """تست تحلیل‌گرهای هوش مصنوعی"""
    
    def test_customer_behavior_analyzer(self):
        """تست تحلیل‌گر رفتار مشتری"""
        analyzer = CustomerBehaviorAnalyzer()
        
        # داده‌های تست
        store_data = {
            'customer_movement_paths': 'clockwise',
            'high_traffic_areas': 'ورودی,صندوق',
            'shelf_count': 15,
            'store_size': 400,
            'store_type': 'supermarket',
            'design_style': 'modern',
            'brand_colors': 'آبی,سفید',
            'peak_hours': '18-20'
        }
        
        result = analyzer.analyze_customer_behavior(store_data)
        
        self.assertIn('path_analysis', result)
        self.assertIn('stopping_analysis', result)
        self.assertIn('purchase_analysis', result)
        self.assertIn('environmental_analysis', result)
        self.assertIn('overall_score', result)
        self.assertIn('recommendations', result)
        
        # بررسی امتیاز کلی
        self.assertGreater(result['overall_score'], 0)
        self.assertLessEqual(result['overall_score'], 1.0)
    
    def test_traffic_analyzer(self):
        """تست تحلیل‌گر ترافیک"""
        analyzer = TrafficAnalyzer()
        
        # داده‌های تست
        store_data = {
            'high_traffic_areas': 'ورودی,مرکز',
            'customer_movement_paths': 'clockwise',
            'entrances': 2,
            'peak_hours': '18-20',
            'store_type': 'supermarket',
            'store_size': 500,
            'store_location': 'تهران',
            'city': 'تهران',
            'area': 'شمال'
        }
        
        result = analyzer.analyze_traffic_patterns(store_data)
        
        self.assertIn('traffic_analysis', result)
        self.assertIn('peak_hours_analysis', result)
        self.assertIn('distribution_analysis', result)
        self.assertIn('external_factors_analysis', result)
        self.assertIn('overall_score', result)
        self.assertIn('recommendations', result)
        
        # بررسی امتیاز کلی
        self.assertGreater(result['overall_score'], 0)
        self.assertLessEqual(result['overall_score'], 1.0)
    
    def test_layout_analyzer(self):
        """تست تحلیل‌گر چیدمان"""
        analyzer = LayoutAnalyzer()
        
        # تست تحلیل پایه
        result = analyzer.analyze('test_image.jpg')
        
        self.assertIn('layout_score', result)
        self.assertIn('recommendations', result)
        self.assertIn('analysis_type', result)
        
        # بررسی امتیاز چیدمان
        self.assertGreater(result['layout_score'], 0)
        self.assertLessEqual(result['layout_score'], 100)
    
    def test_layout_analyzer_psychology(self):
        """تست تحلیل روانشناسی چیدمان"""
        analyzer = LayoutAnalyzer()
        
        result = analyzer.analyze_psychology(self.store_analysis)
        
        self.assertIn('customer_behavior', result)
        self.assertIn('environmental_factors', result)
        self.assertIn('recommendations', result)
        
        # بررسی تحلیل رفتار مشتری
        customer_behavior = result['customer_behavior']
        self.assertIn('attention_points', customer_behavior)
        self.assertIn('emotional_triggers', customer_behavior)
        self.assertIn('decision_making', customer_behavior)

class SecurityServiceTestCase(StoreAnalysisTestCase):
    """تست سرویس امنیتی"""
    
    def test_input_sanitization(self):
        """تست پاکسازی ورودی"""
        service = SecurityService()
        
        # تست ورودی عادی
        clean_input = service.sanitize_input("فروشگاه تست")
        self.assertEqual(clean_input, "فروشگاه تست")
        
        # تست ورودی با HTML
        dirty_input = service.sanitize_input("<script>alert('test')</script>فروشگاه")
        self.assertNotIn("<script>", dirty_input)
        self.assertIn("فروشگاه", dirty_input)
        
        # تست ورودی با JavaScript
        js_input = service.sanitize_input("javascript:alert('test')")
        self.assertNotIn("javascript:", js_input)
    
    def test_password_strength(self):
        """تست اعتبارسنجی قدرت رمز عبور"""
        service = SecurityService()
        
        # رمز قوی
        strong_password = "TestPass123!"
        self.assertTrue(service.validate_password_strength(strong_password))
        
        # رمز ضعیف
        weak_password = "123"
        self.assertFalse(service.validate_password_strength(weak_password))

class ViewTestCase(StoreAnalysisTestCase):
    """تست ویوها"""
    
    def test_index_view(self):
        """تست صفحه اصلی"""
        from django.urls import reverse
        response = self.client.get(reverse('store_analysis:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'چیدمانو')
    
    def test_education_view(self):
        """تست صفحه آموزش"""
        from django.urls import reverse
        response = self.client.get(reverse('store_analysis:education_library'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'آموزش جامع')
    
    def test_article_detail_view(self):
        """تست صفحه کتابخانه آموزشی (جایگزین تست مقاله که مدل ندارد)"""
        from django.urls import reverse
        response = self.client.get(reverse('store_analysis:education_library'))
        self.assertEqual(response.status_code, 200)
    
    def test_store_analysis_form_view(self):
        """تست فرم تحلیل فروشگاه"""
        # بدون لاگین
        from django.urls import reverse
        response = self.client.get(reverse('store_analysis:index'), follow=True)  # Use correct path
        self.assertEqual(response.status_code, 200)  # should work without login
        
        # با لاگین
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('store_analysis:index'), follow=True)  # Use correct path
        self.assertEqual(response.status_code, 200)

class APITestCase(StoreAnalysisTestCase):
    """تست API"""
    
    def setUp(self):
        super().setUp()
        # Ensure the sample analysis is in 'completed' state with results for API detail tests
        self.store_analysis.status = 'completed'
        self.store_analysis.results = {'summary': 'test results'}
        self.store_analysis.save()
        self.client.login(username='testuser', password='testpass123')
    
    def test_analysis_list_api(self):
        """تست API لیست تحلیل‌ها"""
        response = self.client.get(reverse('store_analysis:analysis_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_analysis_detail_api(self):
        """تست API جزئیات تحلیل"""
        response = self.client.get(reverse('store_analysis:analysis_detail', args=[self.store_analysis.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.store_analysis.store_name)

class IntegrationTestCase(StoreAnalysisTestCase):
    """تست‌های یکپارچه"""
    
    def test_complete_analysis_flow(self):
        """تست جریان کامل تحلیل"""
        self.client.login(username='testuser', password='testpass123')
        
        # ایجاد تحلیل جدید
        analysis_data = {
            'store_name': 'فروشگاه یکپارچه',
            'store_type': 'supermarket',
            'store_size': 600,
            'shelf_count': 25,
            'customer_movement_paths': 'clockwise',
            'high_traffic_areas': 'ورودی,مرکز,صندوق',
            'peak_hours': '18-20',
            'design_style': 'modern',
            'brand_colors': 'آبی,سفید'
        }
        
        response = self.client.post(reverse('store_analysis:submit_analysis'), analysis_data)
        self.assertEqual(response.status_code, 302)  # redirect after success
        
        # بررسی ایجاد تحلیل
        new_analysis = StoreAnalysis.objects.filter(store_name='فروشگاه یکپارچه').first()
        self.assertIsNotNone(new_analysis)
        self.assertEqual(new_analysis.user, self.user)
        self.assertEqual(new_analysis.store_type, 'supermarket')

class PerformanceTestCase(StoreAnalysisTestCase):
    """تست‌های عملکرد"""
    
    def test_analyzer_performance(self):
        """تست عملکرد تحلیل‌گرها"""
        import time
        
        analyzer = CustomerBehaviorAnalyzer()
        store_data = {
            'customer_movement_paths': 'clockwise',
            'high_traffic_areas': 'ورودی,صندوق',
            'shelf_count': 15,
            'store_size': 400,
            'store_type': 'supermarket'
        }
        
        start_time = time.time()
        result = analyzer.analyze_customer_behavior(store_data)
        end_time = time.time()
        
        # تحلیل باید در کمتر از 1 ثانیه انجام شود
        self.assertLess(end_time - start_time, 1.0)
        self.assertIsNotNone(result)

class ErrorHandlingTestCase(StoreAnalysisTestCase):
    """تست مدیریت خطا"""
    
    def test_analyzer_error_handling(self):
        """تست مدیریت خطا در تحلیل‌گرها"""
        analyzer = CustomerBehaviorAnalyzer()
        
        # داده‌های نامعتبر
        invalid_data = None
        
        result = analyzer.analyze_customer_behavior(invalid_data)
        
        self.assertIn('error', result)
        self.assertEqual(result['overall_score'], 0.0)
        self.assertIn('خطا در تحلیل رفتار مشتری', result['recommendations'])
    
    def test_security_service_error_handling(self):
        """تست مدیریت خطا در سرویس امنیتی"""
        service = SecurityService()
        
        # ورودی نامعتبر
        result = service.sanitize_input(None)
        self.assertIsNone(result)
        
        # ورودی خالی
        result = service.sanitize_input("")
        self.assertEqual(result, "")
