import urllib.request, os, concurrent.futures as cf
from PIL import Image, ImageDraw
ids = "4239146 4239091 4239035 4239013 4239119 4239031 4108715 4107120 4107284 4108712 4099238 4099354 6197116 6195125 6195111 6197122 6195275 6197108 5591581 4239060 6196692 6197119 6195129 4440565 3990359 4176531 6195951 6197124 4107108 4108710 4239130 4239038".split()
os.makedirs("tools/pexels", exist_ok=True)
def get(i):
    p = f"tools/pexels/{i}.jpg"
    if os.path.exists(p): return i, True
    try:
        req = urllib.request.Request(f"https://images.pexels.com/photos/{i}/pexels-photo-{i}.jpeg?auto=compress&cs=tinysrgb&w=1600", headers={"User-Agent": "Mozilla/5.0"})
        open(p, "wb").write(urllib.request.urlopen(req, timeout=30).read()); return i, True
    except Exception as e:
        return i, str(e)
with cf.ThreadPoolExecutor(8) as ex: res = list(ex.map(get, ids))
ok = [i for i, r in res if r is True]
print("fail", [i for i, r in res if r is not True])
W, H = 300, 220; cols = 6; rows = (len(ok) + cols - 1) // cols
sh = Image.new("RGB", (cols * W, rows * (H + 18)), "white"); d = ImageDraw.Draw(sh)
for n, i in enumerate(ok):
    im = Image.open(f"tools/pexels/{i}.jpg").convert("RGB"); sz = im.size; im.thumbnail((W, H))
    x, y = (n % cols) * W, (n // cols) * (H + 18); sh.paste(im, (x, y)); d.text((x + 3, y + H + 3), f"{i} {sz[0]}x{sz[1]}", fill="black")
sh.save("tools/pexels_sheet.jpg", quality=85)
