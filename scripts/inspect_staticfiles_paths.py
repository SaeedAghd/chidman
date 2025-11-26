import json
p='staticfiles/staticfiles.json'
with open(p, 'r', encoding='utf-8') as f:
    j=json.load(f)
paths=j.get('paths',{})
print('total paths:', len(paths))
for k in sorted(paths.keys()):
    if 'logo' in k or 'images/logo.png' in k:
        print(k,'->',paths[k])
