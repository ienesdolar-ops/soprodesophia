import re
import json
import os

with open('amazon_store.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Procura por blocos com ASIN, título e imagem
# Amazon store carrega itens de produtos em blocos com data attributes ou HTML tags
items = re.findall(r'<img[^>]+src="(https://m\.media-amazon\.com/images/I/[^"]+)"[^>]*alt="([^"]*)"', html)
if not items:
    items = re.findall(r'alt="([^"]+)"[^>]*src="(https://m\.media-amazon\.com/images/I/[^"]+)"', html)
    items = [(src, alt) for alt, src in items]

# Procura por qualquer texto perto de m.media-amazon.com/images/I/
raw_matches = re.findall(r'https://m\.media-amazon\.com/images/I/([A-Za-z0-9%_\-\.]+\.(?:jpg|png))', html)

# Procura por titulos no HTML
titles = re.findall(r'class="[^\"]*a-size-[^\"]*"[^>]*>\s*([^<]+?\b(?:Gnosis|Sophia|Código|Code|Matrix|Aham|Mukti|Hacker|Ego|Spark|Chispa|Capella|Faces|Iavé|Yahvé|Jesus|Cristo|Frequency|Monad|Mónada|Consciência|Conciencia)\b[^<]*)\s*<', html, re.IGNORECASE)

print("Títulos encontrados no HTML da Amazon:")
for t in set(titles):
    print(" -", t.strip())

# Vamos varrer a pasta assets/img/amazon_covers para listar os arquivos baixados
files = os.listdir('assets/img/amazon_covers')
print(f"\nTotal de arquivos de capas de livros na pasta assets/img/amazon_covers: {len(files)}")
for f in files:
    print("Cover file:", f)
