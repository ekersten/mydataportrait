from PIL import Image, ImageFont, ImageDraw
from portrait import Selection

#Read image
size = (900,900)
im = Image.new('RGBA', size , (255,255,255,0))
pixels = im.load();
for x in range(size[0]):
	for y in range(size[1]):
		pixels[x,y] = (255,255,255,255)

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', im.size, (255,255,255,0))

# get a font
fnt = ImageFont.truetype('Verlag Black.otf', 40)
# get a drawing context
d = ImageDraw.Draw(txt)

value = "Lorem ipsun Lorem ipsun Lorem ipsun Lorem ipsun Lorem ipsun Lorem ipsun".upper()
# draw text, half opacity
d.text((10,10), value, font=fnt, fill=(245,242,242,128))
# draw text, full opacity
d.text((10,60), value, font=fnt, fill=(245,242,242,255))

out = Image.alpha_composite(im, txt)

out.save('img/text.jpg')


