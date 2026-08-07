import urllib.request
import re

asins = [
    ('es', 'B0HD9H9L6L'),
    ('en', 'B0HD9KDTZK'),
    ('fr', 'B0HDCP9BXZ'),
    ('de', 'B0HDD3D5S9'),
    ('it', 'B0HDDC5X2R')
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for lang, asin in asins:
    url = f'https://www.amazon.com.br/dp/{asin}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        title_match = re.search(r'<title>(.*?)</title>', html)
        if title_match:
            t = title_match.group(1).split('|')[0].split(':')[0].strip()
            print(f'{lang.upper()} ({asin}): {t.encode("utf-8")}')
        else:
            print(f'{lang.upper()} ({asin}): Sem titulo no HTML')
    except Exception as e:
        print(f'{lang.upper()} ({asin}): Erro {e}')
