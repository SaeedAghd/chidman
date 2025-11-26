#!/usr/bin/env python3
"""
Fix escaped triple-quote sequences in store_analysis/views.py
Replaces occurrences of backslash-escaped quotes (\") with plain quotes (")
"""
from pathlib import Path

p = Path("store_analysis/views.py")
data = p.read_bytes()

# Replace occurrences of backslash + quote (\" ) with quote (")
fixed = data.replace(b'\\\"', b'\"')

if fixed != data:
    p.write_bytes(fixed)
    print("Fixed escaped quotes in", p)
else:
    print("No escaped quotes found in", p)


