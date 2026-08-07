from PIL import Image

img_path = "assets/img/logo-amazon.png"
im = Image.open(img_path)

# Se tiver canal alpha ou branco, pegar bounding box do conteúdo não-transparente/não-branco
if im.mode != 'RGBA':
    im = im.convert('RGBA')

# Obter bounding box do conteúdo visível
# Bounding box baseada em pixels não transparentes
bbox = im.getbbox()

if bbox:
    cropped = im.crop(bbox)
    # Adicionar uma margem sutil de 20px em volta
    w, h = cropped.size
    margin = 20
    new_im = Image.new('RGBA', (w + margin * 2, h + margin * 2), (0, 0, 0, 0))
    new_im.paste(cropped, (margin, margin))
    new_im.save(img_path, "PNG")
    print(f"Capa Amazon recortada com sucesso. Tamanho original: {im.size}, Novo tamanho: {new_im.size}")
