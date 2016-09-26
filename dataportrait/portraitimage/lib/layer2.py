import threading
from . import Paragraph
from PIL import Image, ImageDraw, ImageChops

#process for the thread that creates the first layer
class layer2Thread (threading.Thread):
    def __init__(self, threadID, lock, image, selection, filename):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.lock = lock
        self.image = image
        self.selection = selection
        self.filename = filename

    def run(self):
        #print("Starting " + self.name)
        # Get lock to synchronize threads
        self.lock.acquire()

        pixels = self.image.load()
        for x in range(self.image.width):
            for y in range(self.image.height):
                pixels[(x,y)] = (pixels[(x,y)][0],pixels[(x,y)][1],pixels[(x,y)][2],50)

        foreground = Image.new('RGBA', self.image.size, (0,118,190,100))

        #out = Image.alpha_composite(self.image, foreground)
        out = ImageChops.screen(self.image, foreground)

        pix = out.load()
        for x in range(out.width):
            for y in range(out.height):
                if(not self.selection.selected(x,y)):
                    pix[(x,y)] = (0,0,0,0)

        out.save(self.filename)

        # Free lock to release next thread
        self.lock.release()