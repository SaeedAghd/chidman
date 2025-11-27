#!/usr/bin/env python3
import os
import sys
import django
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chidmano.settings")
django.setup()

from store_analysis.models import ServicePackage

def print_packages():
    pkgs = ServicePackage.objects.filter(is_active=True).order_by('sort_order','price')
    for p in pkgs:
        print(f"package_type={p.package_type!r} name={p.name!r} price={p.price} currency={p.currency} max_analyses={p.max_analyses} validity_days={p.validity_days}")

if __name__ == "__main__":
    print_packages()


