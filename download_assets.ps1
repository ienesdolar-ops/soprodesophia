$base = "https://osoprodesophia.com.br/_assets/media"

# Book covers - mapped by UIClap ID
$covers = @{
    "book-ua154948" = "9f00f2ecbb82e37f5d429f3e63e883f2.jpg"
    "book-ua154926" = "6e500729e8fe109cfd5648231901f257.png"
    "book-ua154939" = "fb4d188c4f80ff0cd8436c69beeda4cc.jpg"
    "book-ua155102" = "9708a5385846d01256775a80b5e6a8e5.jpg"
    "book-ua155651" = "4e774f179cc3882d6c4d8fd5397ae0e9.png"
    "book-ua155673" = "6de38f2c7c659c85de133c84303998ba.jpg"
    "book-ua157756" = "be6cfd197fe3cff36e8c4e033b511503.jpg"
    "book-ua157757" = "14a6bb3da1710e8a39823645ac5d2321.png"
    "book-ua157828" = "2c76b1220b18978e4949a2815ede8003.png"
    "book-ua159156" = "d041e7dd832a316180a0b8988824ecc9.png"
    "book-ua163487" = "035011e180e91e1cf9b15dd4d5b65815.jpg"
    "book-ua163490" = "2af7fe82a8af79a535f0f27c15280bfc.jpg"
    "book-ua179836" = "0516f5a4cd70eb7a49f48fba1becf409.jpg"
}

# Supporting assets
$assets = @{
    "hero-bg" = "05ebe501d71b2cb13b11a9a1700ee34c.png"
    "author-photo" = "90dc983e6166935aec9dbe9ebe0860df.png"
    "logo-amazon" = "355ecf6d9920a315ef8287c73e132fdc.png"
    "logo-uiclap" = "d01938275a7717ac132d4d05b075bb77.png"
    "separator" = "d4338a550d52978466215e2efe3fafaa.svg"
    "spanish-flag" = "34e8f9f91576aa0c1d9ba887602d63fe.png"
    "lang-icon" = "b84ba83d53631075d324dff7c308583d.png"
}

$youtube = @{
    "youtube-banner" = "5875f09aa4de3b5cd8f5013a1d9bd3bf.png"
    "youtube-banner-svg" = "9b1329ac5522c9533fc85bec03027c21.svg"
}

Write-Host "Baixando capas dos livros..." -ForegroundColor Cyan
foreach ($entry in $covers.GetEnumerator()) {
    $ext = [System.IO.Path]::GetExtension($entry.Value)
    $outFile = "assets\img\covers\$($entry.Key)$ext"
    $url = "$base/$($entry.Value)"
    Write-Host "  -> $($entry.Key)$ext"
    try {
        Invoke-WebRequest -Uri $url -OutFile $outFile -UseBasicParsing -ErrorAction Stop
    } catch {
        Write-Host "    ERRO: $_" -ForegroundColor Red
    }
}

Write-Host "`nBaixando assets de suporte..." -ForegroundColor Cyan
foreach ($entry in $assets.GetEnumerator()) {
    $ext = [System.IO.Path]::GetExtension($entry.Value)
    $outFile = "assets\img\$($entry.Key)$ext"
    $url = "$base/$($entry.Value)"
    Write-Host "  -> $($entry.Key)$ext"
    try {
        Invoke-WebRequest -Uri $url -OutFile $outFile -UseBasicParsing -ErrorAction Stop
    } catch {
        Write-Host "    ERRO: $_" -ForegroundColor Red
    }
}

Write-Host "`nBaixando assets YouTube..." -ForegroundColor Cyan
foreach ($entry in $youtube.GetEnumerator()) {
    $ext = [System.IO.Path]::GetExtension($entry.Value)
    $outFile = "assets\img\$($entry.Key)$ext"
    $url = "$base/$($entry.Value)"
    Write-Host "  -> $($entry.Key)$ext"
    try {
        Invoke-WebRequest -Uri $url -OutFile $outFile -UseBasicParsing -ErrorAction Stop
    } catch {
        Write-Host "    ERRO: $_" -ForegroundColor Red
    }
}

# Favicon
Write-Host "`nBaixando favicon..." -ForegroundColor Cyan
try {
    Invoke-WebRequest -Uri "https://osoprodesophia.com.br/_assets/images/2d0b56e7e51cf11036ad8734bdb67e2d.png" -OutFile "assets\img\favicon.png" -UseBasicParsing -ErrorAction Stop
    Write-Host "  -> favicon.png"
} catch {
    Write-Host "    ERRO favicon: $_" -ForegroundColor Red
}

Write-Host "`nDownload concluido!" -ForegroundColor Green
