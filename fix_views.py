#!/usr/bin/env python3
"""
Script to fix indentation issues in store_analysis/views.py
"""

import re

def fix_try_except_blocks(content):
    """Fix try-except block indentation issues"""
    
    # Pattern to find try blocks with incorrect indentation
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for try: followed by incorrectly indented code
        if re.match(r'^(\s*)try:\s*$', line):
            indent_level = len(re.match(r'^(\s*)', line).group(1))
            fixed_lines.append(line)
            i += 1
            
            # Fix the next few lines that should be indented
            while i < len(lines) and lines[i].strip() and not re.match(r'^(\s*)(except|finally|else):', lines[i]):
                next_line = lines[i]
                if next_line.strip():  # Skip empty lines
                    # Ensure proper indentation (4 spaces more than try)
                    current_indent = len(re.match(r'^(\s*)', next_line).group(1))
                    if current_indent <= indent_level:
                        # Fix indentation
                        fixed_line = ' ' * (indent_level + 4) + next_line.strip()
                        fixed_lines.append(fixed_line)
                    else:
                        fixed_lines.append(next_line)
                else:
                    fixed_lines.append(next_line)
                i += 1
            
            # Add the except/finally block
            if i < len(lines):
                fixed_lines.append(lines[i])
                i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    return '\n'.join(fixed_lines)

def main():
    """Main function to fix the views.py file"""
    
    # Read the file
    with open('store_analysis/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix try-except blocks
    fixed_content = fix_try_except_blocks(content)
    
    # Write back to file
    with open('store_analysis/views.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Fixed try-except blocks in store_analysis/views.py")

if __name__ == "__main__":
    main()
