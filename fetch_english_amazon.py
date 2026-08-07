import urllib.request
import os
import json

english_books = [
    {
        "asin": "B0H637BR5T",
        "title": "Texts by Sophia: First Season",
        "url": "https://www.amazon.com.br/TEXTS-SOPHIA-SEASON-Textos-English-ebook/dp/B0H637BR5T"
    },
    {
        "asin": "B0GHPR9C4Y",
        "title": "The Faces of Yahweh & The 13th Element",
        "url": "https://www.amazon.com.br/FACES-YAHWEH-13th-Element-English-ebook/dp/B0GHPR9C4Y"
    },
    {
        "asin": "B0GSW7P2YP",
        "title": "I Am the Spirit, I Am Freedom",
        "url": "https://www.amazon.com.br/Am-Spirit-Freedom-English-ebook/dp/B0GSW7P2YP"
    },
    {
        "asin": "B0GSW8ZGFS",
        "title": "The Alchemy of Shadows",
        "url": "https://www.amazon.com.br/Alchemy-Shadows-English-Fontain-Franco-ebook/dp/B0GSW8ZGFS"
    },
    {
        "asin": "B0GT1FFBDJ",
        "title": "The 10th Portal: Practical Alchemy of the Zero Point",
        "url": "https://www.amazon.com.br/10th-Portal-Practical-Alchemy-English-ebook/dp/B0GT1FFBDJ"
    },
    {
        "asin": "B0D7GF52X5",
        "title": "The Sacred Within the Matrix",
        "url": "https://www.amazon.com.br/Sacred-Within-Matrix-English-ebook/dp/B0D7GF52X5"
    },
    {
        "asin": "B0GSSCSQ6H",
        "title": "Awakening in the Matrix: Gnosis, Dreams & Ego Liberation",
        "url": "https://www.amazon.com.br/Awakening-Matrix-Gnosis-Liberation-English-ebook/dp/B0GSSCSQ6H"
    },
    {
        "asin": "B0GSS9XVKS",
        "title": "Hacker Gnosis: From Exile of Capella to Christic Frequency",
        "url": "https://www.amazon.com.br/Hacker-Gnosis-Capella-Christic-Frequency-ebook/dp/B0GSS9XVKS"
    },
    {
        "asin": "B0GSS9C4K2",
        "title": "Aham Mukti: The Awakening of the Code and the Spark",
        "url": "https://www.amazon.com.br/Aham-Mukti-Awakening-Spark-English-ebook/dp/B0GSS9C4K2"
    },
    {
        "asin": "B0GMXZQCX3",
        "title": "Dialogue between Logic and the Spark: Simulation Score",
        "url": "https://www.amazon.com.br/Dialogue-between-Logic-Spark-Simulation-ebook/dp/B0GMXZQCX3"
    },
    {
        "asin": "B0GM1249XB",
        "title": "The Alliance of Lights and Cosmic Reintegration",
        "url": "https://www.amazon.com.br/Alliance-Lights-Cosmic-Reintegration-English-ebook/dp/B0GM1249XB"
    },
    {
        "asin": "B0GLQZ9GHX",
        "title": "The Code That Became Gnosis: Monad Tuning",
        "url": "https://www.amazon.com.br/Became-Gnosis-Arontic-Software-English-ebook/dp/B0GLQZ9GHX"
    },
    {
        "asin": "B0GHSJRYPC",
        "title": "Who Has Eyes Let Him See: Breath of Sophia",
        "url": "https://www.amazon.com.br/WHO-HAS-EYES-LET-HIM-ebook/dp/B0GHSJRYPC"
    }
]

os.makedirs('assets/img/amazon_en', exist_ok=True)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

for book in english_books:
    asin = book["asin"]
    img_urls = [
        f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01.LZZZZZZZ.jpg",
        f"https://m.media-amazon.com/images/P/{asin}.01._SCLZZZZZZZ_SX500_.jpg",
        f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01.MAIN._SCRM_.jpg"
    ]
    
    success = False
    filename = f"en_{asin}.jpg"
    filepath = os.path.join('assets/img/amazon_en', filename)
    
    for url in img_urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                if len(data) > 5000:
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    print(f"Sucesso [{asin}]: Baixado de {url} ({len(data)} bytes)")
                    book["local_img"] = f"assets/img/amazon_en/{filename}"
                    success = True
                    break
        except Exception as e:
            continue
            
    if not success:
        print(f"Falha ao baixar imagem para {asin}")

with open('english_amazon_books.json', 'w', encoding='utf-8') as f:
    json.dump(english_books, f, indent=2, ensure_ascii=False)
