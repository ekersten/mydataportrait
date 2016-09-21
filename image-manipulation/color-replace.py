from PIL import Image, ImageFilter

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

#Data is an array of tuples, each one a RGB color (r,g,b)
pixels = im.load()

#print pixels
x=0
y=0
while y < im.height:
	while x < im.width:
		if matches(pixels[x,y]):
			pixels[x,y] = (255,255,255)
		x += 1
	y += 1
	x=0

#print list(data)
#im.putData(data,1.0)

im.save('img/replaced.jpg');
#Display image
#im.show()