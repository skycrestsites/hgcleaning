from playwright.sync_api import sync_playwright
from PIL import Image
def warm(pg):
    h = pg.evaluate("document.body.scrollHeight")
    for y in range(0, h, 500):
        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(60)
    pg.wait_for_timeout(800)
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("http://localhost:8765/", wait_until="load", timeout=30000); warm(pg)
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500); pg.screenshot(path="v_hero.png")
    shots = []
    for sel in ["#services", "#about", "main > section:nth-of-type(4)", "main > section:nth-of-type(5)", "#reviews"]:
        el = pg.query_selector(sel); el.scroll_into_view_if_needed(); pg.wait_for_timeout(250)
        el.screenshot(path="tmp.png"); im = Image.open("tmp.png").convert("RGB"); shots.append(im.resize((im.width // 2, im.height // 2)))
    H = sum(i.height for i in shots) + 10 * len(shots); sh = Image.new("RGB", (shots[0].width, H), "#999"); y = 0
    for i in shots: sh.paste(i, (0, y)); y += i.height + 10
    sh.save("v_desk.jpg", quality=82)
    m = b.new_context(**p.devices["iPhone 13"]).new_page()
    m.goto("http://localhost:8765/", wait_until="load", timeout=30000); warm(m)
    ims = []
    for sel in ["body", ".hero__mosaic", "#services", "#about", "main > section:nth-of-type(4)", "#reviews"]:
        if sel == "body": m.evaluate("window.scrollTo(0,0)")
        else:
            m.eval_on_selector(sel, "e => window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 80)")
        m.wait_for_timeout(350); m.screenshot(path="tmp.png"); im = Image.open("tmp.png").convert("RGB"); ims.append(im.resize((im.width // 2, im.height // 2)))
    W = sum(i.width for i in ims) + 10 * len(ims); sh = Image.new("RGB", (W, ims[0].height), "#999"); x = 0
    for i in ims: sh.paste(i, (x, 0)); x += i.width + 10
    sh.save("v_mobile.jpg", quality=85)
    print("scrollWidth", m.evaluate("document.documentElement.scrollWidth"))
    b.close()
