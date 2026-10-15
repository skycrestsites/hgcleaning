from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("http://localhost:8765/", wait_until="load", timeout=30000)
    h = pg.evaluate("document.body.scrollHeight")
    for y in range(0, h, 700):
        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(80)
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(800)
    pg.screenshot(path="n_hero.png")
    for i, sel in enumerate(["#services", "#about", "main > section:nth-of-type(4)", "#reviews", "#areas"]):
        el = pg.query_selector(sel); el.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        el.screenshot(path=f"n_s{i}.png")
    m = b.new_context(**p.devices["iPhone 13"]).new_page()
    m.goto("http://localhost:8765/", wait_until="load", timeout=30000); m.wait_for_timeout(800)
    m.screenshot(path="n_m0.png")
    m.evaluate("window.scrollTo(0, 700)"); m.wait_for_timeout(500); m.screenshot(path="n_m1.png")
    el = m.query_selector("#services"); el.scroll_into_view_if_needed(); m.wait_for_timeout(600); m.evaluate("window.scrollBy(0, 150)"); m.wait_for_timeout(400); m.screenshot(path="n_m2.png")
    b.close()
from PIL import Image
ims = [Image.open(f"n_m{i}.png") for i in range(3)]
W = sum(i.width for i in ims) + 40; sh = Image.new("RGB", (W, ims[0].height), "#999"); x = 0
for im in ims: sh.paste(im, (x, 0)); x += im.width + 20
sh.resize((sh.width // 2, sh.height // 2)).save("n_mobile.jpg", quality=85)
