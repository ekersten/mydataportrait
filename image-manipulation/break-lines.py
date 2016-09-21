from PIL import Image, ImageFont, ImageDraw
from portrait import Selection, Paragraph

def breakLines(font, text, size):
	words = text.split()

	carry = words[0] 
	line = 0
	paragraphs = []

	#Watch out, this is a unusual loop, read carefully before updating
	for i in range(1, len(words)):
		carrySize = font.getsize(carry)
		print "carry of: "+carry+" = ("+str(carrySize[0])+","+str(carrySize[1])+")"
		print str(i) + " - " + str(len(words))
		if	(carrySize[0] > size[0]) or ((i+1) >= len(words)) :

			position = (0, line*carrySize[1])
			par = Paragraph.Paragraph(carry, position)
			paragraphs.append(par)
			carry = words[i]
			line +=1;
		else:
			carry += " " + words[i]
	return paragraphs

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

value = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ut aliquet est. Sed convallis dignissim justo nec porta. Sed volutpat, purus et efficitur porta, justo dui ornare eros, eget dictum dui massa nec massa. Nunc finibus gravida euismod. Praesent quis dui pellentesque, egestas nibh sit amet, fermentum dolor. Donec viverra pretium elementum. Proin fermentum velit a nibh rutrum feugiat. Aliquam vehicula lorem quis justo pretium egestas. Aliquam erat volutpat. Suspendisse vestibulum tempor dui, ac mollis dolor pellentesque et. Vestibulum pharetra vel mauris eu egestas. Sed at placerat ligula. In hac habitasse platea dictumst. Etiam semper sollicitudin velit et hendrerit. Mauris eu pharetra libero.Aliquam vel tortor nec urna semper aliquam. Etiam at ante blandit, faucibus neque at, eleifend urna. Ut urna odio, tempor non ex nec, tristique volutpat sem. Quisque libero lorem, pulvinar in faucibus non, vulputate ut elit. Phasellus scelerisque lacinia mi, ut euismod felis mollis id. Cras pulvinar massa non ultricies ullamcorper. Mauris orci tellus, malesuada sed pellentesque rhoncus, condimentum sed sem. Praesent nibh felis, sagittis mollis mi id, varius fermentum felis.".upper()
paragraphs = breakLines(fnt,value,size)

for p in paragraphs:
	if(p.position[1] < size[1]):
		d.text(p.position, p.text, font=fnt, fill=(245,242,242,128))
	print p

#d.text((10,60), value, font=fnt, fill=(245,242,242,255))

out = Image.alpha_composite(im, txt)

out.save('img/broken.jpg')


