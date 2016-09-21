import numpy as np
from PIL import Image, ImageFilter

#Read image
im = Image.open( 'img/portrait1.jpg' )

im=im.convert('L') #makes it greyscale
y=np.asarray(im.getdata(),dtype=np.float64).reshape((im.size[1],im.size[0]))


y=np.asarray(y,dtype=np.uint8) #if values still in range 0-255! 
im=Image.fromarray(y,mode='L')

im.save('img/grey.jpg');