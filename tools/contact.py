from PIL import Image, ImageDraw
import os
d = "Stock images"
files = sorted(os.listdir(d))
W, H = 360, 270
cols = 4
rows = (len(files)+cols-1)//cols
sheet = Image.new("RGB", (cols*W, rows*(H+24)), "white")
dr = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(os.path.join(d, f)).convert("RGB")
    print(f, im.size)
    im.thumbnail((W, H))
    x, y = (i%cols)*W, (i//cols)*(H+24)
    sheet.paste(im, (x, y))
    dr.text((x+4, y+H+4), f"{i}: {f}", fill="black")
sheet.save("tools/contact.jpg", quality=85)
