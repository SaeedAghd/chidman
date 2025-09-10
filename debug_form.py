#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from store_analysis.forms import AIStoreAnalysisForm

def test_form_fields():
    """Test if form fields are properly defined"""
    print("Testing AIStoreAnalysisForm fields...")
    
    form = AIStoreAnalysisForm()
    
    # Check if page-5 fields exist
    page5_fields = [
        'checkout_count',
        'checkout_location', 
        'aisle_width',
        'shelf_spacing',
        'problem_areas',
        'restricted_areas',
        'attraction_elements'
    ]
    
    print("\nChecking page-5 fields:")
    for field_name in page5_fields:
        if field_name in form.fields:
            field = form.fields[field_name]
            print(f"✅ {field_name}: {type(field).__name__}")
            if hasattr(field, 'widget'):
                print(f"   Widget: {type(field.widget).__name__}")
                if hasattr(field.widget, 'attrs'):
                    print(f"   Attrs: {field.widget.attrs}")
        else:
            print(f"❌ {field_name}: NOT FOUND")
    
    print(f"\nTotal form fields: {len(form.fields)}")
    print("All form field names:")
    for field_name in form.fields.keys():
        print(f"  - {field_name}")

def test_form_rendering():
    """Test form rendering"""
    print("\n" + "="*50)
    print("Testing form rendering...")
    
    form = AIStoreAnalysisForm()
    
    # Test rendering specific fields
    print("\nRendering checkout_count:")
    try:
        rendered = form['checkout_count']
        print(f"✅ Rendered successfully: {rendered}")
    except Exception as e:
        print(f"❌ Error rendering checkout_count: {e}")
    
    print("\nRendering restricted_areas:")
    try:
        rendered = form['restricted_areas']
        print(f"✅ Rendered successfully: {rendered}")
    except Exception as e:
        print(f"❌ Error rendering restricted_areas: {e}")

if __name__ == "__main__":
    test_form_fields()
    test_form_rendering()
