from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    ctx = b.new_context(**p.devices["iPhone 13"])
    pg = ctx.new_page()
    pg.goto("http://localhost:8765/", wait_until="load", timeout=30000)
    pg.click(".menu-toggle"); pg.wait_for_timeout(500)
    pg.screenshot(path="x_menu.png")
    pg.click(".menu-toggle"); pg.wait_for_timeout(300)
    pg.click(".mobile-bar .btn--primary"); pg.wait_for_timeout(5000)
    pg.screenshot(path="x_book.png")
    b.close()
