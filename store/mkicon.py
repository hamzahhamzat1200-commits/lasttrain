from PIL import Image, ImageDraw, ImageFilter
import math, random
random.seed(7)
def scene(W,H,train_scale=1.0,tx=.5,ty=.72):
    S=2; w,h=W*S,H*S
    im=Image.new('RGB',(w,h))
    px=im.load()
    # sky gradient: deep navy -> teal horizon -> warm rim
    for y in range(h):
        t=y/h
        top=(6,13,30); mid=(22,58,86); low=(120,92,80)
        if t<.62:
            k=t/.62; c=tuple(int(top[i]+(mid[i]-top[i])*k) for i in range(3))
        else:
            k=(t-.62)/.38; c=tuple(int(mid[i]+(low[i]-mid[i])*k) for i in range(3))
        for x in range(w): px[x,y]=c
    # aurora
    au=Image.new('RGBA',(w,h),(0,0,0,0)); ad=ImageDraw.Draw(au)
    for b,(col,off) in enumerate([((60,230,190),0),((120,120,255),.07)]):
        pts=[]
        for i in range(0,w+20,20):
            x=i; y=h*(.22+off)+math.sin(i/w*5+b)*h*.05
            pts.append((x,y))
        for i in range(len(pts)-1):
            ad.polygon([pts[i],pts[i+1],(pts[i+1][0],pts[i+1][1]+h*.28),(pts[i][0],pts[i][1]+h*.28)],fill=col+(40,))
    au=au.filter(ImageFilter.GaussianBlur(h*.03)); im.paste(au,(0,0),au)
    d=ImageDraw.Draw(im,'RGBA')
    # stars
    for _ in range(int(W*H/2200)):
        x=random.random()*w; y=random.random()*h*.5; r=random.random()*1.6*S/2+.5
        d.ellipse([x-r,y-r,x+r,y+r],fill=(220,235,255,random.randint(90,230)))
    # mountains
    def mtn(base,amp,seed,col):
        random.seed(seed); pts=[(0,h)]
        for i in range(0,w+40,40):
            y=base-amp*(.5+.5*math.sin(i/w*6+seed))*(.6+.4*random.random())
            pts.append((i,y))
        pts.append((w,h)); d.polygon(pts,fill=col)
    mtn(h*.66,h*.20,1,(24,52,78,255)); mtn(h*.72,h*.14,3,(14,34,54,255))
    # ground
    gy=h*ty+h*.07
    d.rectangle([0,gy,w,h],fill=(8,18,32,255))
    # rail
    d.rectangle([0,gy-2*S,w,gy+2*S],fill=(70,90,110,255))
    # train
    sc=train_scale*w/512; cx=w*tx; base=gy-4*S
    def box(x0,y0,x1,y1,c): d.rounded_rectangle([cx+x0*sc,base+y0*sc,cx+x1*sc,base+y1*sc],radius=6*sc,fill=c)
    # tender/coal car
    box(-215,-62,-70,-8,(26,40,58,255)); box(-205,-78,-80,-60,(8,12,20,255))
    # cab
    box(-70,-112,5,-8,(32,52,76,255)); box(-76,-120,11,-108,(190,215,235,255))
    box(-58,-96,-18,-60,(255,170,70,255)); box(-8,-96,-2,-60,(255,170,70,200))
    # boiler
    box(5,-84,150,-8,(30,46,68,255)); box(150,-78,162,-14,(20,32,48,255))
    # chimney
    box(110,-122,132,-84,(14,22,34,255)); box(104,-130,138,-120,(14,22,34,255))
    # dome
    d.ellipse([cx+50*sc,base-104*sc,cx+86*sc,base-70*sc],fill=(38,58,84,255))
    # headlamp glow
    gl=Image.new('RGBA',(w,h),(0,0,0,0)); g=ImageDraw.Draw(gl)
    hx=cx+162*sc; hy=base-46*sc
    g.polygon([(hx,hy-6*sc),(w,hy-40*sc),(w,hy+14*sc),(hx,hy+6*sc)],fill=(255,210,130,45))
    g.ellipse([cx-60*sc,base-110*sc,cx+20*sc,base-40*sc],fill=(255,150,60,60))
    gl=gl.filter(ImageFilter.GaussianBlur(10*S)); im.paste(gl,(0,0),gl)
    d=ImageDraw.Draw(im,'RGBA')
    d.ellipse([hx-6*sc,hy-6*sc,hx+6*sc,hy+6*sc],fill=(255,235,180,255))
    # wheels
    for wx,r in [(-175,15),(-120,15),(-40,24),(30,24),(100,22)]:
        x=cx+wx*sc; y=base-r*sc+2*sc; rr=r*sc
        d.ellipse([x-rr,y-rr,x+rr,y+rr],fill=(8,14,24,255),outline=(90,112,134,255),width=int(2*sc))
        for a in range(0,360,45):
            d.line([x,y,x+math.cos(math.radians(a))*rr*.9,y+math.sin(math.radians(a))*rr*.9],fill=(90,112,134,255),width=max(1,int(1.4*sc)))
    # steam
    st=Image.new('RGBA',(w,h),(0,0,0,0)); s=ImageDraw.Draw(st)
    sx=cx+121*sc; sy=base-132*sc
    for i in range(7):
        r=(10+i*5)*sc; x=sx-(i*14+math.sin(i*1.7)*10)*sc; y=sy-i*17*sc
        s.ellipse([x-r,y-r,x+r,y+r],fill=(205,225,242,max(14,135-i*17)))
    st=st.filter(ImageFilter.GaussianBlur(7*S)); im.paste(st,(0,0),st)
    # snow flakes
    d=ImageDraw.Draw(im,'RGBA')
    for _ in range(int(W*H/3500)):
        x=random.random()*w; y=random.random()*h; r=random.random()*2*S/2+.6
        d.ellipse([x-r,y-r,x+r,y+r],fill=(235,245,255,150))
    return im.resize((W,H),Image.LANCZOS)
# 512 icon (full-bleed square, Play applies its own mask)
ic=scene(512,512,train_scale=1.0,tx=.52,ty=.80); ic.save('icon-512.png')
# feature graphic
fg=scene(1024,500,train_scale=.62,tx=.40,ty=.76); fg.save('feature-1024x500.png')
# launcher icons
import os
for name,sz in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
    os.makedirs(f'res/mipmap-{name}',exist_ok=True)
    ic.resize((sz,sz),Image.LANCZOS).save(f'res/mipmap-{name}/ic_launcher.png')
