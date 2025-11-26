import os
for root,dirs,files in os.walk('staticfiles'):
    for f in files:
        if 'guides' in root.replace('\\','/'):
            print(os.path.join(root,f))
