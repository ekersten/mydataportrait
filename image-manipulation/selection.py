from PIL import Image, ImageFilter
from portrait import Selection

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
im = Image.open( 'img/portrait1.jpg' )

#selection = []

#Data is an array of tuples, each one a RGB color (r,g,b)
pixels = im.load()

selection = Selection.Selection(im.width, im.height)
selection.select(pixels, matches)

for x in range(im.width):
	for y in range(im.height):
		if(selection.selected(x,y)):
			pixels[x,y] = (0,255,0)

im.save('img/selected.jpg')


