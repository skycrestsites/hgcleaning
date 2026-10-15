import sys, asyncio
from playwright.sync_api import sync_playwright
from PIL import Image
pages = sys.argv[1:] or ["/"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    ctx = b.new_context(**p.devices["iPhone 13"])
    pg = ctx.new_page()
    for path in pages:
        pg.goto("http://localhost:8765" + path, wait_until="networkidle")
        name = "m_" + (path.strip("/").replace("/", "_") or "home")
        sw = pg.evaluate("document.documentElement.scrollWidth")
        print(path, "scrollWidth", sw, "viewport", pg.viewport_size["width"])
        pg.screenshot(path=name + ".png", full_page=True)
        im = Image.open(name + ".png").convert("RGB")
        im = im.resize((im.width // 2, im.height // 2))
        n = 0
        for i in range(0, im.height, 1100):
            im.crop((0, i, im.width, min(i + 1100, im.height))).save(f"{name}_{n}.jpg", quality=80); n += 1
        print(name, im.size, n)
    # menu open
    pg.goto("http://localhost:8765/", wait_until="networkidle")
    pg.click(".menu-toggle"); pg.wait_for_timeout(500)
    pg.screenshot(path="m_menu.png")
    b.close()
