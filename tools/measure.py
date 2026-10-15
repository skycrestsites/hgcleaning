from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    m = b.new_context(**p.devices["iPhone 13"]).new_page()
    m.goto("http://localhost:8765/", wait_until="load", timeout=30000); m.wait_for_timeout(500)
    for sel in [".hero-split", ".hero-split__media", ".hero-split__media > img", ".book-panel", "#services", "#services .section-head"]:
        print(sel, m.eval_on_selector(sel, "e => { const r = e.getBoundingClientRect(); return [Math.round(r.top + scrollY), Math.round(r.height)] }"))
    b.close()
