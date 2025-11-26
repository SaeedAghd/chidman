import os
for root,dirs,files in os.walk('staticfiles'):
    for f in files:
        if 'icon-192' in f or 'screenshot' in f or 'shortcut-' in f:
            print(os.path.join(root,f))
