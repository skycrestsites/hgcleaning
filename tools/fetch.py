import urllib.request, os, concurrent.futures as cf
from PIL import Image, ImageDraw
ids = """1581578731548-c64695cc6952 1563453392212-326f5e854473 1497366216548-37526070297c 1621905251189-08b45d6a269e
1600566753086-00f18fb6b3ea 1584622650111-993a426fbf0a 1527515637462-cff94eecc1ac 1558317374-067fb5f30001
1556911220-bff31c812dba 1556909114-f6e7ad7d3136 1522708323590-d24dbb6b0267 1502672260266-1c1ef2d93688
1560448204-e02f11c3d0e2 1631049307264-da0ec9d70304 1503387762-592deb58ef4e 1504307651254-35680f356dfd
1600585154340-be6161a56a0c 1564013799919-ab600027ffc6 1484154218962-a197022b5858 1556228453-efd6c1ff04f6
1586023492125-27b2c045efd7 1568605114967-8130f3a36994 1524758631624-e2822e304c36 1497215728101-856f4ea42174
1628177142898-93e36e4e3a50 1585421514738-01798e348b17 1610557892470-55d9e80c0bce 1626806787461-102c1bfaaea1
1556761175-5973dc0f32e7 1600880292203-757bb62b4baf 1595526114035-0d45ed16cfbf 1570129477492-45c003edd2be
1582268611958-ebfd161ef9cf 1556020685-ae41abfc9365 1574269909862-7e1d70bb8078 1600210492486-724fe5c67fb0
1600607687939-ce8a6c25118c 1615874959474-d609969a20ed 1594026112284-02bb6f3352fe 1527515545081-5db817172677""".split()
os.makedirs("tools/online", exist_ok=True)
def get(i):
    p = f"tools/online/{i}.jpg"
    if os.path.exists(p): return i, True
    try:
        req = urllib.request.Request(f"https://images.unsplash.com/photo-{i}?w=1400&q=80&fm=jpg", headers={"User-Agent":"Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read()
        open(p,"wb").write(data); return i, True
    except Exception as e:
        return i, str(e)
with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(get, ids))
ok = [i for i,r in res if r is True]
for i,r in res:
    if r is not True: print("FAIL", i, r)
W,H=300,200; cols=5; rows=(len(ok)+cols-1)//cols
sheet = Image.new("RGB",(cols*W, rows*(H+18)),"white"); dr=ImageDraw.Draw(sheet)
for n,i in enumerate(ok):
    im=Image.open(f"tools/online/{i}.jpg").convert("RGB"); im.thumbnail((W,H))
    x,y=(n%cols)*W,(n//cols)*(H+18); sheet.paste(im,(x,y)); dr.text((x+3,y+H+3),f"{n}: {i}",fill="black")
sheet.save("tools/online_sheet.jpg",quality=85)
print(len(ok),"ok")
