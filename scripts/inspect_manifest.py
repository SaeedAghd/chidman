import json
with open('staticfiles/manifest.json', 'r', encoding='utf-8') as f:
    m=json.load(f)
keys = sorted(m.keys())
print('Total keys in manifest:', len(keys))
for k in keys[:60]:
    print(k, '->', m[k])
