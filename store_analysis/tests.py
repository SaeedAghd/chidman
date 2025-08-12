from django.test import TestCase
from .forms import StoreAnalysisForm
from django.contrib.auth.models import User

class StoreAnalysisFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.valid_data = {
            'store_name': 'فروشگاه تست',
            'store_location': 'تهران',
            'store_type': 'supermarket',
            'store_size': 100,
            'store_dimensions': '10 m x 8 m',
            'entrances': 2,
            'shelf_count': 5,
            'shelf_dimensions': '2x1',
            'shelf_contents': 'مواد غذایی',
            'checkout_location': 'سمت راست',
            'unused_areas': '',
            'product_categories': ['groceries'],
            'top_products': 'برنج، روغن',
            'sales_volume': 5000000,
            'pos_system': 'POS',
            'has_surveillance': False,
            'camera_count': 0,
            'camera_locations': '',
            'camera_coverage': '',
            'has_customer_video': False,
            'video_duration': 0,
            'customer_movement_paths': 'clockwise',
            'customer_path_notes': 'توضیح تست',
            'design_style': '',
            'brand_colors': '',
            'decorative_elements': '',
            'layout_restrictions': '',
            'morning_sales_percent': 25,
            'noon_sales_percent': 25,
            'evening_sales_percent': 25,
            'night_sales_percent': 25,
            'main_entrance': 'front',
            'customer_traffic': 'medium',
            'main_lighting': 'natural',
            'unused_area_type': '',
            'unused_area_size': 0,
            'unused_area_reason': '',
        }

    def test_form_valid_with_minimal_data(self):
        form = StoreAnalysisForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_valid_without_sales_volume(self):
        data = self.valid_data.copy()
        data['sales_volume'] = ''
        form = StoreAnalysisForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_valid_without_unused_area_type(self):
        data = self.valid_data.copy()
        data['unused_area_type'] = ''
        form = StoreAnalysisForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_valid_with_invalid_unused_area_type(self):
        data = self.valid_data.copy()
        data['unused_area_type'] = 'invalid_option'
        form = StoreAnalysisForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
