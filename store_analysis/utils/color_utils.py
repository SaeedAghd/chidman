# -*- coding: utf-8 -*-
"""
Color utilities for converting color names to HEX codes
"""

# Mapping of Persian color names to HEX codes
PERSIAN_COLOR_MAP = {
    # Basic colors
    'قرمز': '#FF0000',
    'آبی': '#0000FF',
    'سبز': '#00FF00',
    'زرد': '#FFFF00',
    'سفید': '#FFFFFF',
    'مشکی': '#000000',
    'خاکستری': '#808080',
    'نارنجی': '#FFA500',
    'بنفش': '#800080',
    'صورتی': '#FFC0CB',
    'قهوه‌ای': '#A52A2A',
    'طلایی': '#FFD700',
    'نقره‌ای': '#C0C0C0',
    
    # Light colors
    'قرمز روشن': '#FF6B6B',
    'آبی روشن': '#87CEEB',
    'سبز روشن': '#90EE90',
    'زرد روشن': '#FFFFE0',
    'صورتی روشن': '#FFB6C1',
    'نارنجی روشن': '#FFB366',
    
    # Dark colors
    'قرمز تیره': '#8B0000',
    'آبی تیره': '#00008B',
    'سبز تیره': '#006400',
    'خاکستری تیره': '#696969',
    'قهوه‌ای تیره': '#654321',
    
    # Special colors
    'آبی آسمانی': '#87CEEB',
    'سبز دریایی': '#2E8B57',
    'قرمز شرابی': '#722F37',
    'آبی دریایی': '#4682B4',
    'سبز زیتونی': '#808000',
    'قرمز گیلاسی': '#DE3163',
    'آبی کبالت': '#0047AB',
    'سبز نعنایی': '#98FB98',
    'زرد لیمویی': '#FFFACD',
    'نارنجی هویجی': '#FF8C00',
    'بنفش ارغوانی': '#8A2BE2',
    'صورتی گلابی': '#FF69B4',
    'طلایی کهربایی': '#FFBF00',
    'نقره‌ای پلاتینی': '#E5E4E2',
}

# Mapping of English color names to HEX codes
ENGLISH_COLOR_MAP = {
    'red': '#FF0000',
    'blue': '#0000FF',
    'green': '#00FF00',
    'yellow': '#FFFF00',
    'white': '#FFFFFF',
    'black': '#000000',
    'gray': '#808080',
    'grey': '#808080',
    'orange': '#FFA500',
    'purple': '#800080',
    'pink': '#FFC0CB',
    'brown': '#A52A2A',
    'gold': '#FFD700',
    'silver': '#C0C0C0',
    'light red': '#FF6B6B',
    'light blue': '#87CEEB',
    'light green': '#90EE90',
    'light yellow': '#FFFFE0',
    'light pink': '#FFB6C1',
    'light orange': '#FFB366',
    'dark red': '#8B0000',
    'dark blue': '#00008B',
    'dark green': '#006400',
    'dark gray': '#696969',
    'dark grey': '#696969',
    'dark brown': '#654321',
    'sky blue': '#87CEEB',
    'sea green': '#2E8B57',
    'wine red': '#722F37',
    'navy blue': '#4682B4',
    'olive green': '#808000',
    'cherry red': '#DE3163',
    'cobalt blue': '#0047AB',
    'mint green': '#98FB98',
    'lemon yellow': '#FFFACD',
    'carrot orange': '#FF8C00',
    'purple violet': '#8A2BE2',
    'peach pink': '#FF69B4',
    'amber gold': '#FFBF00',
    'platinum silver': '#E5E4E2',
}


def color_name_to_hex(color_input):
    """
    Convert color name to HEX code
    
    Args:
        color_input (str): Color name in Persian or English, or HEX code
        
    Returns:
        str: HEX code (e.g., '#FF0000')
    """
    if not color_input:
        return None
    
    # Clean input
    color_input = color_input.strip().lower()
    
    # If it's already a HEX code, return it
    if color_input.startswith('#') and len(color_input) == 7:
        return color_input.upper()
    
    # Check Persian color names
    if color_input in PERSIAN_COLOR_MAP:
        return PERSIAN_COLOR_MAP[color_input]
    
    # Check English color names
    if color_input in ENGLISH_COLOR_MAP:
        return ENGLISH_COLOR_MAP[color_input]
    
    # If not found, return the original input
    return color_input


def get_color_suggestions():
    """
    Get list of available color names for suggestions
    
    Returns:
        list: List of color names
    """
    persian_colors = list(PERSIAN_COLOR_MAP.keys())
    english_colors = list(ENGLISH_COLOR_MAP.keys())
    return persian_colors + english_colors


def validate_color_input(color_input):
    """
    Validate color input (name or HEX)
    
    Args:
        color_input (str): Color input
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not color_input:
        return False
    
    color_input = color_input.strip().lower()
    
    # Check if it's a valid HEX code
    if color_input.startswith('#') and len(color_input) == 7:
        try:
            int(color_input[1:], 16)
            return True
        except ValueError:
            return False
    
    # Check if it's a known color name
    return (color_input in PERSIAN_COLOR_MAP or 
            color_input in ENGLISH_COLOR_MAP)
