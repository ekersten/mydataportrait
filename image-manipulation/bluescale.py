import numpy as np
from PIL import Image, ImageFilter, ImageChops, ImageEnhance
from portrait import Selection

#draw selection layer on plain white
def matches(color):
	c = (51,156,126)
	tolerance = 30

	if( (c[0] - tolerance) <= color[0] <= (c[0] + tolerance) and 
		(c[1] - tolerance) <= color[1] <= (c[1] + tolerance) and 
		(c[2] - tolerance) <= color[2] <= (c[2] + tolerance)
		):	
		return True
	return False

#Read image
im = Image.open( 'img/portrait1.jpg').convert('RGBA')


enhancer = ImageEnhance.Contrast(im)
enhancer.enhance(0.8)


pixels = im.load();

#create the croma selection to be used later on
selection = Selection.Selection(im.width, im.height)
selection.select(pixels, matches)

for x in range(im.size[0]):
	for y in range(im.size[1]):
		avg = ( pixels[x,y][0] + pixels[x,y][1] + pixels[x,y][2] )/3
		pixels[x,y] = (avg,avg,avg,255)

#create an image with solid blue and opacity
blue = Image.new('RGBA', im.size)
pixels = blue.load();
for x in range(blue.size[0]):
	for y in range(blue.size[1]):
		pixels[x,y] = (0,118,190,80)

#out = Image.alpha_composite(im, blue)
out = ImageChops.screen(im, blue)


##also merge the background text
mask = Image.open( 'img/broken.jpg').convert('RGBA')
pixels = mask.load()
selection.invert()
for x in range(im.width):
	for y in range(im.height):
		if(selection.selected(x,y)):
			pixels[x,y] = (pixels[x,y][0], pixels[x,y][1], pixels[x,y][2], 0)

out = Image.alpha_composite(out, mask)




out.save('img/blue.jpg');