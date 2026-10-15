from PIL import Image, ImageDraw, ImageFont, ImageOps
W, H = 1200, 630
og = Image.new("RGB", (W, H), (1, 23, 41))
photo = ImageOps.fit(Image.open("assets/img/team-cleaning-living-room.webp").convert("RGB"), (520, H))
og.paste(photo, (W - 520, 0))
d = ImageDraw.Draw(og)
d.rectangle((W - 520, 0, W - 516, H), fill=(11, 120, 220))
logo = Image.open("tools/logo_white_full.png") if False else Image.open("assets/img/logo-white.png")
lw = 560
logo = logo.resize((lw, round(lw * logo.height / logo.width)), Image.LANCZOS)
og.paste(logo, (60, 120), logo)
f1 = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 40)
f2 = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 26)
d.text((62, 360), "Elevating Clean", font=f1, fill=(255, 255, 255))
d.text((62, 418), "Residential and commercial cleaning", font=f2, fill=(190, 205, 222))
d.text((62, 454), "Salt Lake City, UT and surrounding areas", font=f2, fill=(190, 205, 222))
d.rectangle((62, 520, 122, 524), fill=(11, 120, 220))
og.save("assets/og-image.jpg", quality=86)
