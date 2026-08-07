import urllib.request
import re
import json

url = 'https://www.amazon.com.br/stores/Lean-Fontain-Franco/author/B0GHG1476S?ref=ap_rdr&shoppingPortalEnabled=true'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6'
}

req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        with open('amazon_author_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Página da Amazon salva com sucesso! Tamanho:", len(html))
        
        # Encontrar imagens de alta resolução m.media-amazon.com
        imgs = set(re.findall(r'https://m\.media-amazon\.com/images/I/[A-Za-z0-9%_\-\.]+\.(?:jpg|png)', html))
        print(f"Total de imagens encontradas: {len(imgs)}")
        for img in imgs:
            print("IMG:", img)
except Exception as e:
    print("Erro ao acessar Amazon:", e)
