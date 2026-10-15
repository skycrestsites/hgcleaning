import sys
from playwright.sync_api import sync_playwright
from PIL import Image
path, prefix = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    ctx = b.new_context(**p.devices["iPhone 13"]) if len(sys.argv) < 4 else b.new_context(viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    pg.goto("http://localhost:8765" + path, wait_until="load", timeout=30000)
    # trigger lazy loads
    h = pg.evaluate("document.body.scrollHeight")
    for y in range(0, h, 600):
        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(60)
    pg.wait_for_timeout(1200)
    secs = pg.query_selector_all("main > section, body > footer")
    imgs = []
    for i, s in enumerate(secs):
        cls = s.get_attribute("class") or ""
        if "booking" in cls:
            continue
        s.scroll_into_view_if_needed(); pg.wait_for_timeout(150)
        f = f"{prefix}_s{i}.png"; s.screenshot(path=f); imgs.append(Image.open(f).convert("RGB"))
    # tile 4 per row
    imgs = [im.resize((im.width // 2, im.height // 2)) for im in imgs]
    for g in range(0, len(imgs), 4):
        grp = imgs[g:g+4]; W = sum(x.width + 10 for x in grp); H = max(x.height for x in grp)
        sh = Image.new("RGB", (W, H), "#999"); x = 0
        for im in grp: sh.paste(im, (x, 0)); x += im.width + 10
        sh.save(f"{prefix}_t{g//4}.jpg", quality=80)
    print(len(imgs), "sections")
    b.close()


