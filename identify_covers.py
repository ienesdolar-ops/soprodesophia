import os
import json
import urllib.request
import re

files = [f for f in os.listdir('assets/img/amazon_covers') if f.endswith(('.jpg', '.png'))]
print(f"Total de capas da Amazon a identificar: {len(files)}")

# Vamos checar os tamanhos das imagens para ordenar por maior resolução
files_sorted = sorted(files, key=lambda x: os.path.getsize(os.path.join('assets/img/amazon_covers', x)), reverse=True)

for f in files_sorted[:15]:
    size = os.path.getsize(os.path.join('assets/img/amazon_covers', f))
    print(f"Capa Amazon: {f} ({size} bytes)")
