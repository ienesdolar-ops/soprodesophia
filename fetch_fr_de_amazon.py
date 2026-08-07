import urllib.request
import os
import json

intl_books = [
    {
        "asin": "B0H8PJ1CXH",
        "lang": "fr",
        "title": "Textes de Sophia: PREMIÈRE SAISON",
        "url": "https://www.amazon.com.br/Textes-Sophia-PREMI%C3%88RE-SAISON-French-ebook/dp/B0H8PJ1CXH"
    },
    {
        "asin": "B0H992D47Z",
        "lang": "de",
        "title": "Texte von Sophia: ERSTE STAFFEL",
        "url": "https://www.amazon.com.br/Texte-von-Sophia-STAFFEL-German-ebook/dp/B0H992D47Z"
    }
]

os.makedirs('assets/img/amazon_intl', exist_ok=True)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

for book in intl_books:
    asin = book["asin"]
    lang = book["lang"]
    img_urls = [
        f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01.LZZZZZZZ.jpg",
        f"https://m.media-amazon.com/images/P/{asin}.01._SCLZZZZZZZ_SX500_.jpg"
    ]
    
    success = False
    filename = f"{lang}_{asin}.jpg"
    filepath = os.path.join('assets/img/amazon_intl', filename)
    
    for url in img_urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                if len(data) > 5000:
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    print(f"Sucesso [{asin}]: Baixado {filename} ({len(data)} bytes)")
                    book["local_img"] = f"assets/img/amazon_intl/{filename}"
                    success = True
                    break
        except Exception as e:
            continue
            
    if not success:
        print(f"Falha ao baixar imagem para {asin}")

with open('intl_amazon_books.json', 'w', encoding='utf-8') as f:
    json.dump(intl_books, f, indent=2, ensure_ascii=False)
