import os
import pytesseract
from PIL import Image

covers_dir = 'assets/img/amazon_covers'
files = [f for f in os.listdir(covers_dir) if f.endswith(('.jpg', '.png'))]

results = []

for f in sorted(files, key=lambda x: os.path.getsize(os.path.join(covers_dir, x)), reverse=True):
    path = os.path.join(covers_dir, f)
    try:
        img = Image.open(path)
        # OCR com pytesseract
        text = pytesseract.image_to_string(img).strip()
        clean_text = " ".join(text.split())
        
        lang = "DESCONHECIDO"
        txt_upper = clean_text.upper()
        
        if any(w in txt_upper for w in ['THE ', 'OF ', 'AND ', 'TO ', 'FROM ', 'CHRISTIC', 'EXILE', 'AWAKENING', 'CODE THAT']):
            lang = "ENGLISH"
        elif any(w in txt_upper for w in ['EL ', 'DEL ', 'CONVIRTIÓ', 'LAS ', 'DESPERTAR DEL', 'CHISPA', 'SOPLO']):
            lang = "ESPAÑOL"
        elif any(w in txt_upper for w in ['DO ', 'DA ', 'DE ', 'VIROU', 'QUE ', 'FÍSICA', 'CENTELHA', 'A ', 'O ']):
            lang = "PORTUGUÊS"
            
        results.append({
            'file': f,
            'size': os.path.getsize(path),
            'lang': lang,
            'text': clean_text
        })
    except Exception as e:
        print(f"Erro em {f}: {e}")

print("=== RESULTADO DA CLASSIFICAÇÃO DAS CAPAS DA AMAZON ===")
for r in results:
    print(f"[{r['lang']}] {r['file']} ({r['size']} bytes)")
    print(f"   Texto: {r['text'][:150]}")
    print("-" * 50)

with open('amazon_classified.json', 'w', encoding='utf-8') as out_f:
    import json
    json.dump(results, out_f, indent=2, ensure_ascii=False)
