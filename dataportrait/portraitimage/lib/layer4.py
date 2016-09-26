import threading
from . import Paragraph
from PIL import Image

#process for the thread that creates the first layer
class layer4Thread (threading.Thread):
    def __init__(self, threadID, lock, files, size, layerFile):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.lock = lock
        self.files = files
        self.size = size
        self.layerFile = layerFile

    def run(self):
        #print("Starting " + self.name)
        # Get lock to synchronize threads
        self.lock.acquire()

        background = Image.new('RGBA', self.size, (255,255,255,0))

        #add headline
        headline = self.files[0]
        img = Image.open(headline, 'r')
        img_w, img_h = img.size
        offset = ((self.size[0] - img_w) // 2, 80)
        background.paste(img, offset)
        
        logo = self.files[1]
        img = Image.open(logo, 'r')
        img_w, img_h = img.size
        offset = ((self.size[0] - img_w) - 20, (self.size[1] - img_h)//2)
        background.paste(img, offset)
        background.save(self.layerFile)

        # Free lock to release next thread
        self.lock.release()