import re
import json
import os
import urllib.request

with open('amazon_store.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

os.makedirs('assets/img/amazon_covers', exist_ok=True)

# Procura por todas as imagens m.media-amazon.com/images/I/
raw_imgs = re.findall(r'https://m\.media-amazon\.com/images/I/[A-Za-z0-9%_\-\.]+\.(?:jpg|png)', html)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36'
}

downloaded = []
seen = set()

for raw_url in raw_imgs:
    # Remove sufixos tipo ._AC_UL320_.jpg
    clean_url = re.sub(r'\._[A-Za-z0-9_,\-]+\.', '.', raw_url)
    filename = os.path.basename(clean_url)
    
    # Ignora pequenas imagens/icones da interface Amazon
    if filename in seen or 'icon' in filename.lower() or 'logo' in filename.lower() or 'sprite' in filename.lower():
        continue
    seen.add(filename)
    
    local_path = os.path.join('assets/img/amazon_covers', filename)
    try:
        req = urllib.request.Request(clean_url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(local_path, 'wb') as out_f:
            out_f.write(resp.read())
        size = os.path.getsize(local_path)
        # Filtra apenas capas de livros (tamanho > 15KB)
        if size > 15000:
            downloaded.append({'url': clean_url, 'file': f"assets/img/amazon_covers/{filename}", 'size': size})
            print(f"Baixado capa Amazon: {filename} ({size} bytes)")
        else:
            os.remove(local_path)
    except Exception as e:
        print(f"Erro ao baixar {clean_url}: {e}")

print(f"\nTotal de capas reais de livros baixadas diretamente da Amazon: {len(downloaded)}")
with open('amazon_covers_downloaded.json', 'w', encoding='utf-8') as out_json:
    json.dump(downloaded, out_json, indent=2)
