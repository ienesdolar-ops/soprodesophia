import re
import json
import urllib.request
import os

with open('amazon_store.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Criar pasta para imagens da Amazon
os.makedirs('assets/img/amazon_covers', exist_ok=True)

# Procurar blocos JSON no HTML da Amazon
json_blocks = re.findall(r'window\.__PRELOADED_STATE__\s*=\s*({.*?});', html, re.DOTALL)
if not json_blocks:
    json_blocks = re.findall(r'data-a-state="([^"]+)"', html)

# Extrair pares de Imagem e Título/Alt do HTML
img_matches = re.findall(r'<img[^>]+src="(https://m\.media-amazon\.com/images/I/[^"]+)"[^>]*alt="([^"]*)"', html)
if not img_matches:
    img_matches = re.findall(r'alt="([^"]*)"[^>]*src="(https://m\.media-amazon\.com/images/I/[^"]+)"', html)
    # inverte a ordem para (url, alt)
    img_matches = [(url, alt) for alt, url in img_matches]

print(f"Total de pares (Imagem, Alt) encontrados: {len(img_matches)}")

books_data = []
seen_imgs = set()

for url, alt in img_matches:
    # Limpa URL da imagem para obter versão de alta resolução
    clean_url = re.sub(r'\._[A-Za-z0-9_,\-]+\.', '.', url)
    if clean_url in seen_imgs or not alt.strip():
        continue
    seen_imgs.add(clean_url)
    
    filename = os.path.basename(clean_url)
    local_path = os.path.join('assets/img/amazon_covers', filename)
    
    books_data.append({
        'alt': alt.strip(),
        'amazon_url': clean_url,
        'local_file': f"assets/img/amazon_covers/{filename}"
    })

print(f"\nLivros extraídos com títulos ({len(books_data)}):")
for b in books_data:
    print(f"Título/Alt: {b['alt']}\nURL: {b['amazon_url']}\n")

# Baixar todas as capas da Amazon
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36'
}

for b in books_data:
    try:
        req = urllib.request.Request(b['amazon_url'], headers=headers)
        with urllib.request.urlopen(req) as resp, open(b['local_file'], 'wb') as f:
            f.write(resp.read())
        print(f"Baixado: {b['local_file']}")
    except Exception as e:
        print(f"Erro ao baixar {b['amazon_url']}: {e}")

with open('amazon_books_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(books_data, f, indent=2, ensure_ascii=False)
