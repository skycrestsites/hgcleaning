import os, urllib.request
from PIL import Image, ImageOps
S = "Stock images/"
O = "tools/online/"
urllib.request.urlretrieve  # noqa
hero_src = "tools/online/hero-2000.jpg"
if not os.path.exists(hero_src):
    req = urllib.request.Request("https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=2200&q=80&fm=jpg", headers={"User-Agent": "Mozilla/5.0"})
    open(hero_src, "wb").write(urllib.request.urlopen(req, timeout=60).read())
def u(i): return O + i + ".jpg"
M = {
  "home-hero": (hero_src, 2000),
  "team-cleaning-living-room": (S + "Cleaning-Movers-2.jpg", 1200),
  "gloved-hand-spraying-surface": (u("1628177142898-93e36e4e3a50"), 1000),
  "bright-clean-living-room": (u("1600566753086-00f18fb6b3ea"), 1600),
  "standard-kitchen-island": (S + "standard-clean.png", 1400),
  "standard-mopping-floor": (S + "mopping cleanin.jpg", 1000),
  "standard-wiping-counter": (S + "cleaning 2.jpg", 1000),
  "standard-white-kitchen": (u("1484154218962-a197022b5858"), 1000),
  "deep-steam-cleaning": (S + "deep clean.jpg", 1400),
  "deep-stovetop-detail": (S + "kitchen clean.png", 1000),
  "deep-grout-scrubbing": (S + "floor cleaning.png", 1000),
  "deep-carpet-extraction": (S + "carpet-cleaning 2.jpg", 1000),
  "recurring-made-bedroom": (S + "bedroom clean 2.jpg", 1400),
  "recurring-vacuuming-bedroom": (S + "bedroom cleaning .jpg", 1000),
  "recurring-tidy-living-room": (u("1560448204-e02f11c3d0e2"), 1000),
  "recurring-bright-bedroom": (u("1595526114035-0d45ed16cfbf"), 1000),
  "move-moving-day-boxes": (S + "move-in Cleaning 2.jpg", 1000),
  "move-empty-carpet-vacuum": (S + "carpet vacuuming 1.jpg", 1000),
  "move-home-exterior": (u("1570129477492-45c003edd2be"), 1400),
  "move-spray-and-wipe": (S + "cleaning 1.jpg", 1000),
  "commercial-office-glass": (S + "commercial cleaning.png", 1400),
  "commercial-office-plants": (u("1497215728101-856f4ea42174"), 1000),
  "commercial-office-corridor": (u("1497366216548-37526070297c"), 1000),
  "commercial-office-lounge": (u("1524758631624-e2822e304c36"), 1000),
  "construction-dust-vacuum": (S + "construction cleaning.jpeg", 1400),
  "construction-floor-machine": (S + "construction cleaning.jpg", 1000),
  "construction-site-renovation": (u("1504307651254-35680f356dfd"), 1000),
  "rental-guest-bedroom": (u("1631049307264-da0ec9d70304"), 1400),
  "rental-apartment-living": (u("1522708323590-d24dbb6b0267"), 1000),
  "rental-cozy-bedroom": (u("1615874959474-d609969a20ed"), 1000),
  "rental-spotless-bathroom": (S + "bathroom clean.png", 1000),
  "addon-kitchen-appliances": (u("1556911220-bff31c812dba"), 1400),
  "addon-laundry-room": (u("1626806787461-102c1bfaaea1"), 1000),
  "addon-interior-windows": (u("1581578731548-c64695cc6952"), 1000),
  "addon-inside-oven": (u("1574269909862-7e1d70bb8078"), 1000),
  "bathroom-modern-clean": (u("1584622650111-993a426fbf0a"), 1000),
}
os.makedirs("assets/img", exist_ok=True)
for name, (src, w) in M.items():
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(f"assets/img/{name}.webp", "WEBP", quality=78, method=6)
    print(name, im.size)
im = Image.open("assets/img/bright-clean-living-room.webp")
