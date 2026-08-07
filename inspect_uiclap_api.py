import urllib.request
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Baixar o JS bundle da UIClap para achar a API de titulos
js_url = 'https://loja.uiclap.com/assets/index-CfwTGOsF.js'
req = urllib.request.Request(js_url, headers=headers)
with urllib.request.urlopen(req) as resp:
    js_content = resp.read().decode('utf-8')

# procurar endpoints de API no JS
endpoints = re.findall(r'https?://[^\s"\']+', js_content)
for ep in set(endpoints):
    if 'api' in ep or 's3' in ep or 'storage' in ep or 'cloudfront' in ep:
        print('Endpoint:', ep)
