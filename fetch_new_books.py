import urllib.request
import re
import os

os.makedirs('assets/img/amazon_es', exist_ok=True)
os.makedirs('assets/img/amazon_en', exist_ok=True)
os.makedirs('assets/img/amazon_intl', exist_ok=True)
os.makedirs('assets/img/covers', exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

amazon_downloads = [
    ('B0HD9H9L6L', 'assets/img/amazon_es/es_B0HD9H9L6L.jpg'),
    ('B0HD9KDTZK', 'assets/img/amazon_en/en_B0HD9KDTZK.jpg'),
    ('B0HDCP9BXZ', 'assets/img/amazon_intl/fr_B0HDCP9BXZ.jpg'),
    ('B0HDD3D5S9', 'assets/img/amazon_intl/de_B0HDD3D5S9.jpg'),
    ('B0HDDC5X2R', 'assets/img/amazon_intl/it_B0HDDC5X2R.jpg')
]

for asin, path in amazon_downloads:
    url = f'https://images-na.ssl-images-amazon.com/images/P/{asin}.01.LZZZZZZZ.jpg'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp, open(path, 'wb') as f:
            f.write(resp.read())
        print(f'Baixado Amazon {asin} -> {path}')
    except Exception as e:
        print(f'Erro ao baixar {asin}: {e}')

# UIClap fetch ua191456
uiclap_url = 'https://loja.uiclap.com/titulo/ua191456/'
uiclap_req = urllib.request.Request(uiclap_url, headers=headers)
try:
    with urllib.request.urlopen(uiclap_req) as resp:
        html = resp.read().decode('utf-8')
    
    og_match = re.search(r'property="og:image"\s+content="([^"]+)"', html)
    if not og_match:
        og_match = re.search(r'content="([^"]+)"\s+property="og:image"', html)
    
    if og_match:
        img_url = og_match.group(1)
        print(f'og:image UIClap: {img_url}')
        img_req = urllib.request.Request(img_url, headers=headers)
        uiclap_path = 'assets/img/covers/book-ua191456.jpg'
        with urllib.request.urlopen(img_req) as resp, open(uiclap_path, 'wb') as f:
            f.write(resp.read())
        print(f'Baixado UIClap -> {uiclap_path}')
    else:
        print('og:image nao encontrado, procurando qualquer imagem da capa...')
        match = re.search(r'https://[^"]*ua191456[^"]*\.(jpg|png|jpeg)', html, re.IGNORECASE)
        if match:
            img_url = match.group(0)
            print(f'Imagem encontrada: {img_url}')
            img_req = urllib.request.Request(img_url, headers=headers)
            uiclap_path = 'assets/img/covers/book-ua191456.jpg'
            with urllib.request.urlopen(img_req) as resp, open(uiclap_path, 'wb') as f:
                f.write(resp.read())
            print(f'Baixado UIClap -> {uiclap_path}')
        else:
            print('Nenhuma imagem encontrada.')
except Exception as e:
    print(f'Erro UIClap: {e}')
