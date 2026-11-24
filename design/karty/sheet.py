import sys
from PIL import Image
out, files = sys.argv[1], sys.argv[2:]
cols = min(8, len(files)); rows = (len(files)+cols-1)//cols
w,h = 300,450
c = Image.new('RGB',(cols*(w+10)+10, rows*(h+10)+10),'#cbbf9f')
for i,f in enumerate(files):
    try: im = Image.open(f).convert('RGB').resize((w,h))
    except Exception: continue
    c.paste(im,(10+(i%cols)*(w+10),10+(i//cols)*(h+10)))
c.save(out)
