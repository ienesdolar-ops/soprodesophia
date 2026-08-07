import re
import json
import os
import urllib.request

with open('amazon_store.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print(f"HTML lido: {len(html)} bytes")

# Procura por blocos de dados JSON ou elementos de produto
# Amazon Author Central armazena os livros num JSON no HTML ou em tags de imagem
image_urls = re.findall(r'https://m\.media-amazon\.com/images/I/([A-Za-z0-9%_\-\.]+\.(?:jpg|png))', html)
print(f"Total de referencias de imagem m.media-amazon.com: {len(image_urls)}")

# Filtrar imagens únicas que parecem capas de livros (geralmente começam com 5.. ou 8.. ou 9..)
unique_imgs = []
seen = set()
for img_name in image_urls:
    # Limpa sufixos de redimensionamento da Amazon tipo ._AC_UL320_.jpg -> .jpg
    clean_name = re.sub(r'\._[A-Za-z0-9_,\-]+\.', '.', img_name)
    base_id = clean_name.split('.')[0]
    if base_id not in seen and not any(x in clean_name.lower() for x in ['icon', 'logo', 'avatar', 'sprite', 'play']):
        seen.add(base_id)
        full_url = f"https://m.media-amazon.com/images/I/{clean_name}"
        unique_imgs.append(full_url)

print("\n--- Capas de livros encontradas na Amazon ---")
for i, url in enumerate(unique_imgs, 1):
    print(f"{i}. {url}")

# Procurar também por títulos e ASINs no HTML
products = []
# Procura por padrão de links de produtos /dp/ASIN ou /gp/product/ASIN
matches = re.findall(r'href="([^"]*/dp/([A-Z0-9]{10})[^"]*)"', html)
asins = set()
for href, asin in matches:
    if asin not in asins:
        asins.add(asin)
        products.append({"asin": asin, "url": f"https://www.amazon.com.br/dp/{asin}"})

print(f"\nTotal de ASINs de livros encontrados: {len(products)}")
for p in products:
    print(p)

with open('amazon_products.json', 'w', encoding='utf-8') as f:
    json.dump({"images": unique_imgs, "products": products}, f, indent=2, ensure_ascii=False)
