from PIL import Image, ImageDraw, ImageFont

# Boş bir beyaz arka plan oluştur
width, height = 600, 300
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Türkçe karakterleri içeren bir metin oluştur
text = "Merhaba Dünya! Türkçe Karakterler: ŞÇĞÜİÖ"

# Kullanılacak yazı tipi ve boyutunu seç
font_size = 20
font = ImageFont.truetype("Comic Sans MS", font_size)

# Metni görüntüye çiz
text_width, text_height = draw.textsize(text, font)
x = (width - text_width) // 2
y = (height - text_height) // 2

draw.text((x, y), text, fill="black", font=font)

# Görüntüyü göster
image.show()
