import threading
import Paragraph
from PIL import Image, ImageDraw, ImageEnhance

#process for the thread that creates the first layer
class baseThread (threading.Thread):
    def __init__(self, threadID, name, image, outputFile):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.image = image
        self.outputFile = outputFile

    def run(self):
		print "Starting " + self.name
		# Get lock to synchronize threads
		#threadLock.acquire()

		pixels = self.image.load();

		for x in range(self.image.size[0]):
			for y in range(self.image.size[1]):
				avg = ( pixels[x,y][0] + pixels[x,y][1] + pixels[x,y][2] )/3
				pixels[x,y] = (avg,avg,avg,255)


		enhancer = ImageEnhance.Contrast(self.image)
		enhancer.enhance(1.5).save(self.outputFile)

		# Free lock to release next thread
		#threadLock.release()