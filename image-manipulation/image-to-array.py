from PIL import Image, ImageFilter
#Read image
im = Image.open( 'img/thumb.jpeg' )

#Data is an array of tuples, each one a RGB color (r,g,b)
data = im.getdata()


#Display image
#im.show()
