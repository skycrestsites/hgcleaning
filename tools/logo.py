from PIL import Image, ImageDraw
from collections import Counter
src = Image.open("image.png").convert("RGB")
W, H = src.size
px = src.load()
blues = Counter()
for y in range(0, H, 3):
    for x in range(0, W, 3):
        r, g, b = px[x, y]
        if b - r > 120 and b > 180: blues[(r//8*8, g//8*8, b//8*8)] += 1
print("blues", blues.most_common(6))

out = Image.new("RGBA", src.size)
op = out.load()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        a = max(255 - r, 255 - g, 255 - b)
        if a < 6:
            op[x, y] = (255, 255, 255, 0); continue
        af = a / 255
        c = [min(255, max(0, round((v - 255 * (1 - af)) / af))) for v in (r, g, b)]
        op[x, y] = (c[0], c[1], c[2], a)
bbox = out.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
print("bbox", bbox)
logo = out.crop(bbox)
logo.save("assets/img/logo.png", optimize=True)

white = logo.copy(); wp = white.load()
for y in range(white.height):
    for x in range(white.width):
        r, g, b, a = wp[x, y]
        if a and not (b - r > 90 and b > 150):
            wp[x, y] = (255, 255, 255, a)
white.save("assets/img/logo-white.png", optimize=True)

# mark = everything left of the vertical divider line
A = logo.getchannel("A").load()
prof = [sum(1 for y in range(logo.height) if A[x, y] > 100) for x in range(logo.width)]
div = next(x for x in range(20, logo.width) if prof[x] == 0) + 8
mark = logo.crop((0, 0, div - 8, logo.height))
mark = mark.crop(mark.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox())
mark.save("tools/mark.png")
wm = white.crop((0, 0, div - 8, white.height))
wm = wm.crop(wm.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox())

def icon(size, pad=0.17, radius=0.22):
    S = size * 4
    base = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(base).rounded_rectangle((0, 0, S - 1, S - 1), radius=int(S * radius), fill=(1, 23, 41, 255))
    m = wm.copy()
    inner = int(S * (1 - 2 * pad))
    k = inner / max(m.width, m.height)
    m = m.resize((round(m.width * k), round(m.height * k)), Image.LANCZOS)
    base.alpha_composite(m, ((S - m.width) // 2, (S - m.height) // 2))
    return base.resize((size, size), Image.LANCZOS)

for name, im in (("logo", logo), ("logo-white", white)):
    w = 640
    im.resize((w, round(w * im.height / im.width)), Image.LANCZOS).save(f"assets/img/{name}.png", optimize=True)
icon(32).save("assets/favicon-32.png")
icon(16, pad=0.12).save("assets/favicon-16.png")
icon(180, radius=0).save("assets/apple-touch-icon.png")
icon(192).save("assets/icon-192.png")
icon(512).save("assets/icon-512.png")
icon(256).save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
icon(512).save("tools/favicon_preview.png")
print("done", logo.size)
pv = Image.new("RGBA", (1600, 1300), (247, 249, 252, 255))
pv.alpha_composite(logo.resize((750, int(750 * logo.height / logo.width))), (20, 20))
dark = Image.new("RGBA", (800, 320), (1, 23, 41, 255))
dark.alpha_composite(white.resize((750, int(750 * white.height / white.width))), (25, 25))
pv.alpha_composite(dark, (800, 0))
pv.alpha_composite(Image.open("tools/favicon_preview.png"), (20, 330))
for i, s in enumerate([180, 64, 32, 16]):
    pv.alpha_composite(icon(s).resize((s, s)), (600 + i * 200, 400))
pv.convert("RGB").save("tools/logo_preview.jpg")
