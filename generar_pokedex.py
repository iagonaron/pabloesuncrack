#!/usr/bin/env python3
"""Regenera pokedex.js a partir de las imágenes de la carpeta pokemon/.
Uso:  python3 generar_pokedex.py            (ejecutar dentro de la carpeta de la app)
Acepta jpg/jpeg/png/webp. Reduce las imágenes a 900px y calcula dos colores por imagen.
Los nombres se toman del nombre del archivo (edítalos luego en Ajustes ⚙️ si quieres)."""
import os, json, re, colorsys
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(HERE,'pokemon')
files=sorted(f for f in os.listdir(D) if f.lower().endswith(('.jpg','.jpeg','.png','.webp')))
def colors(im):
    s=im.convert('RGB').resize((64,64)); b={}
    for r,g,bl in list(s.getdata()):
        h,l,sat=colorsys.rgb_to_hls(r/255,g/255,bl/255)
        if l<.12 or l>.93 or sat<.28: continue
        k=(r>>5,g>>5,bl>>5); e=b.setdefault(k,[0,0,0,0]); e[0]+=1;e[1]+=r;e[2]+=g;e[3]+=bl
    arr=sorted(b.values(),key=lambda e:-e[0])
    if not arr: return ['#ffcb05','#3b6cd6']
    hx=lambda e:'#%02x%02x%02x'%(round(e[1]/e[0]),round(e[2]/e[0]),round(e[3]/e[0]))
    c1=arr[0]; h1=colorsys.rgb_to_hls(c1[1]/c1[0]/255,c1[2]/c1[0]/255,c1[3]/c1[0]/255)[0]*360
    for e in arr[1:]:
        h=colorsys.rgb_to_hls(e[1]/e[0]/255,e[2]/e[0]/255,e[3]/e[0]/255)[0]*360
        dh=abs(h-h1); dh=min(dh,360-dh)
        if dh>40 and e[0]>arr[0][0]*.08: return [hx(c1),hx(e)]
    r,g,bl=colorsys.hls_to_rgb(((h1+150)%360)/360,.5,.7); return [hx(c1),'#%02x%02x%02x'%(int(r*255),int(g*255),int(bl*255))]
out=[]
for f in files:
    p=os.path.join(D,f); im=Image.open(p).convert('RGB')
    if max(im.size)>900: im.thumbnail((900,900)); im.save(p,quality=82,optimize=True)
    nice=re.sub(r'\.[^.]+$','',f); nice=re.sub(r'[_\-]+',' ',nice).strip(); nice=re.sub(r'\s+',' ',nice)[:40]
    if not re.search(r'[A-Za-zÁ-ú]{3,}',nice) or nice.lower() in ('pokemon','pokémon'): nice='Pokémon legendario'
    out.append({'id':f,'name':nice,'file':'pokemon/'+f,'colors':colors(im)})
open(os.path.join(HERE,'pokedex.js'),'w',encoding='utf-8').write('window.POKEDEX_BASE='+json.dumps(out,ensure_ascii=False,indent=1)+';\n')
print('pokedex.js generado con',len(out),'imágenes')
