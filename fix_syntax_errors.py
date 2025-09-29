#!/usr/bin/env python3
"""
Script to fix syntax errors in store_analysis/views.py
"""

import re

def fix_syntax_errors():
    """Fix common syntax errors in views.py"""
    
    # Read the file
    with open('store_analysis/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix patterns
    fixes = [
        # Fix try blocks without proper indentation
        (r'(\s+)try:\s*\n(\s+)from \.models import (\w+)\s*\n(\s+)([^e][^x][^c][^e][^p][^t].*)', 
         r'\1try:\n\2    from .models import \3\n\2    \5'),
        
        # Fix except blocks without proper indentation
        (r'(\s+)except ImportError:\s*\n(\s+)([^e][^x][^c][^e][^p][^t].*)', 
         r'\1except ImportError:\n\2    \3'),
        
        # Fix except Exception blocks
        (r'(\s+)except Exception as e:\s*\n(\s+)([^e][^x][^c][^e][^p][^t].*)', 
         r'\1except Exception as e:\n\2    \3'),
    ]
    
    # Apply fixes
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Write back
    with open('store_analysis/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Syntax errors fixed!")

if __name__ == "__main__":
    fix_syntax_errors()
