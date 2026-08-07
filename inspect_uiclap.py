import urllib.request
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request('https://loja.uiclap.com/titulo/ua191456/', headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

titles = re.findall(r'<title>(.*?)</title>', html)
print('Title:', [t.encode('utf-8') for t in titles])

imgs = re.findall(r'src=["\']([^"\']+)["\']', html)
for img in imgs:
    print('Img:', img)
