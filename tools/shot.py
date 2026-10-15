import subprocess, sys, os, tempfile, uuid
from PIL import Image
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
def shot(url, w, h, name, chunk=1400):
    out = os.path.abspath(f"{name}.png")
    if os.path.exists(out): os.remove(out)
    prof = os.path.join(tempfile.gettempdir(), "edge-" + uuid.uuid4().hex)
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={prof}",
                    f"--window-size={w},{h}", "--virtual-time-budget=6000", f"--screenshot={out}", url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    im = Image.open(out).convert("RGB")
    # trim trailing blank (white) area
    px = im.load()
    bottom = im.height
    while bottom > 100 and all(px[x, bottom - 1] == (255, 255, 255) for x in range(0, im.width, 7)):
        bottom -= 1
    im = im.crop((0, 0, im.width, bottom))
    n = 0
    for i in range(0, im.height, chunk):
        im.crop((0, i, im.width, min(i + chunk, im.height))).save(f"{name}_{n}.jpg", quality=80); n += 1
    print(name, im.size, n, "parts")
if __name__ == "__main__":
    shot(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 1400)
