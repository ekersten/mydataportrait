import threading
import Paragraph
from PIL import Image, ImageDraw

#process for the thread that creates the first layer
class layer2Thread (threading.Thread):
    def __init__(self, threadID, name, image, selection, filename):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.image = image
        self.selection = selection
        self.filename = filename

    def run(self):
		print "Starting " + self.name
		# Get lock to synchronize threads
		#threadLock.acquire()

		foreground = Image.new('RGBA', self.image.size, (0,118,190,80))

		out = Image.alpha_composite(self.image, foreground)
		pixels = out.load()
		for x in range(out.width):
			for y in range(out.height):
				if(not self.selection.selected(x,y)):
					pixels[x,y] = (0,0,0,0)

		out.save(self.filename)

		# Free lock to release next thread
		#threadLock.release()