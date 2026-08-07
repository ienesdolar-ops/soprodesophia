import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

base_url = 'https://storage.googleapis.com/images.uiclap.com/capa/'
asins = ['ua191456']
exts = ['.jpg', '.png', '-1.jpg', '-1.png', '_front.jpg', '_front.png', '-front.jpg']

for asin in asins:
    for ext in exts:
        url = f'{base_url}{asin}{ext}'
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                print(f'Sucesso! {url} ({len(data)} bytes)')
                with open(f'assets/img/covers/book-{asin}.jpg', 'wb') as f:
                    f.write(data)
                break
        except Exception as e:
            pass
