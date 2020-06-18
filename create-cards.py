import re
import textwrap
import random
from PIL import Image, ImageFont, ImageDraw

def manueldecodage_to_unicode(txt):
    repl = [
        ("A","\ua723"),
        ("a","\ua725"),
        ("H","\u1e25"),
        ("x","\u1e2b"),
        ("X","\u1e96"),
        ("S","\u0161"),
        ("T","\u1e6f"),
        ("D","\u1e0f"),
        ("i","j"),
    ]
    for o,r in repl:
        txt = txt.replace(o,r)
    return txt

font = ImageFont.truetype('font/new_athena_unicode.ttf', 100)
fonts = ImageFont.truetype('font/new_athena_unicode.ttf', 80)

path = "new"
outfolder = "anki"
tags = "dict"

cardw = 800
cardh = 500
marginx = 50
marginy = 20

img = []
translit = []
translat = []
with open(path+"/"+path+"1.html", "r") as fi:
    for line in fi:
        if "<img " in line:
            result = re.search('src=\'(.*)\' width(.*)Italic">(\s*)(.*)</font>(.*)(<br/>|</body)', line)
            try:
                img.append(result.group(1))
                translit.append(result.group(4))
                translat.append(result.group(5))
            except AttributeError:
                print("Could not read line:")
                print(line)
N = len(img)
print("Found %d entries in '%s'" % (N,path))

c = list(zip(img,translit,translat))
random.shuffle(c)
img,translit,translat = zip(*c)



with open(outfolder+"/deck.tsv","w") as fo:
    for i in range(N):
        txt1 = manueldecodage_to_unicode(translit[i])
        print(i, txt1, translat[i])

        fo.write("\t\t%s\tcard_front_%05d.png\tcard_back_%05d.png\t\t\n"%(tags,i,i))

        hiero = Image.open(path+"/"+img[i])
        bg = Image.new('RGBA', hiero.size, (255,255,255))
        hiero = Image.alpha_composite(bg, hiero) # set alpha to white
        side1 = Image.new('RGBA', (cardw, cardh), (255, 255, 255))
        ratio1 = hiero.size[0]/(cardw-2.*marginx)
        ratio2 = hiero.size[1]/(cardh-2.*marginy)
        ratio = max(ratio1,ratio2)
        offsetx = int((cardw-hiero.size[0]/ratio-2.*marginx)/2.)
        offsety = int((cardh-hiero.size[1]/ratio-2.*marginy)/2.)
        side1r = hiero.resize((int(hiero.size[0]/ratio),int(hiero.size[1]/ratio)), Image.LANCZOS)

        side1.paste(side1r,(marginx+offsetx,marginy+offsety))
        side1.save(outfolder+'/card_front_%05d.png'%i, 'PNG')


        side2 = Image.new('RGBA', (cardw, cardh), (255, 255, 255))
        draw = ImageDraw.Draw(side2)
        w1, h1 = font.getsize(txt1)
        y_text = marginy
        draw.text(((cardw-w1)/2,y_text), txt1, fill='black', font=font)
        y_text += h1

        y_text += 0.1*h1
        draw.line((marginx,y_text, cardw-marginx,y_text), fill="black")
        y_text += 0.1*h1

        txt2 = translat[i]

        lines = textwrap.wrap(txt2, width=20)
        for line in lines:
            w2, h2 = fonts.getsize(line)

            draw.text(((cardw-w2)/2,y_text), line, fill='black', font=fonts)
            y_text += h2

        side2.save(outfolder+'/card_back_%05d.png'%i, 'PNG')

