import urllib.request
import os

spanish_books = [
    {
        "asin": "B0H6Y342F3",
        "title": "Textos de Sofía - Primera Temporada",
        "url": "https://www.amazon.com.br/Textos-Sofia-Primera-Temporada-Spanish-ebook/dp/B0H6Y342F3"
    },
    {
        "asin": "B0FFH6MKYH",
        "title": "El Código que se Convirtió en Gnosis",
        "url": "https://www.amazon.com.br/C%C3%B3digo-que-Convirti%C3%B3-Gnosis-Sintonizaci%C3%B3n-ebook/dp/B0FFH6MKYH"
    },
    {
        "asin": "B0GHSLNLM2",
        "title": "Quien Tenga Ojos Que Vea",
        "url": "https://www.amazon.com.br/QUIEN-TENGA-OJOS-QUE-VEA-ebook/dp/B0GHSLNLM2"
    },
    {
        "asin": "B0GHRV5NP7",
        "title": "Aham Mukti: El Despertar del Código y la Chispa",
        "url": "https://www.amazon.com.br/Aham-Mukti-Despertar-C%C3%B3digo-Chispa-ebook/dp/B0GHRV5NP7"
    },
    {
        "asin": "B0GLZ7HHDS",
        "title": "La Alianza de las Luces y la Reintegración Cósmica",
        "url": "https://www.amazon.com.br/Alianza-Luces-Reintegraci%C3%B3n-C%C3%B3smica-Sophia-ebook/dp/B0GLZ7HHDS"
    },
    {
        "asin": "B0GMYXRV4R",
        "title": "Diálogo Entre la Lógica y la Chispa",
        "url": "https://www.amazon.com.br/Di%C3%A1logo-Entre-L%C3%B3gica-Chispa-Puntuaci%C3%B3n-ebook/dp/B0GMYXRV4R"
    }
]

os.makedirs('assets/img/amazon_es', exist_ok=True)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

for book in spanish_books:
    asin = book["asin"]
    # Padrão oficial de imagem de alta resolução da Amazon por ASIN
    img_urls = [
        f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01.LZZZZZZZ.jpg",
        f"https://m.media-amazon.com/images/P/{asin}.01._SCLZZZZZZZ_SX500_.jpg",
        f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01.MAIN._SCRM_.jpg"
    ]
    
    success = False
    filename = f"es_{asin}.jpg"
    filepath = os.path.join('assets/img/amazon_es', filename)
    
    for url in img_urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                if len(data) > 5000: # Se for imagem válida e não 1x1 404
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    print(f"Sucesso [{asin}]: Baixado de {url} ({len(data)} bytes)")
                    book["local_img"] = f"assets/img/amazon_es/{filename}"
                    success = True
                    break
        except Exception as e:
            continue
            
    if not success:
        print(f"Falha ao baixar imagem para {asin}")

import json
with open('spanish_amazon_books.json', 'w', encoding='utf-8') as f:
    json.dump(spanish_books, f, indent=2, ensure_ascii=False)
