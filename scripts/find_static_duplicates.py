import os
from pathlib import Path
import sys
import importlib
sys.path.insert(0, r'C:/Users/saeid/OneDrive/Desktop/chideman')
from chidmano import settings

dirs = [Path(p) for p in settings.STATICFILES_DIRS]
# include app static directories
for app in settings.INSTALLED_APPS:
    try:
        mod = importlib.import_module(app)
        mod_path = Path(getattr(mod, '__file__', '')).parent
        app_static = mod_path / 'static'
        if app_static.exists():
            dirs.append(app_static)
    except Exception:
        pass

rel_map = {}
for d in dirs:
    if not d.exists():
        continue
    for root,_,files in os.walk(d):
        for f in files:
            full = Path(root) / f
            rel = os.path.relpath(full, d).replace('\\','/')
            rel_map.setdefault(rel, []).append(str(full))

duplicates = {k:v for k,v in rel_map.items() if len(v)>1}
print(f'Found {len(duplicates)} duplicated relative paths across STATICFILES_DIRS and app static directories')
count=0
for k,v in sorted(duplicates.items())[:500]:
    count+=1
    print(k)
    for p in v:
        print('  -', p)
print('\nTotal duplicates listed:', count)
