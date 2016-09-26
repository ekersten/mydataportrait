import threading
from . import Paragraph
from PIL import Image, ImageDraw

#process for the thread that creates the first layer
class layer1Thread (threading.Thread):
    def __init__(self, threadID, lock, size, filename,text, font, color, lineHeight, selection):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.size = size
        self.lock = lock
        self.filename = filename
        self.text = text
        self.font = font
        self.color = color
        self.lineHeight = lineHeight
        self.selection = selection

    def run(self, ):
        #print("Starting "   +   self.name)
        # Get lock to synchronize threads
        self.lock.acquire()

        #background = Image.new('RGBA', self.size , (255,255,255,255))
        foreground = Image.new('RGBA', self.size, (255,255,255,255))

        #break the lines into single lines
        paragraphs = self.breakLines()
        d = ImageDraw.Draw(foreground)
        for p in paragraphs:
            if(p.position[1] < self.size[1]):
                d.text(p.position, p.text, font=self.font, fill=self.color)
            #print p

        pixels = foreground.load()
        for x in range(self.selection.width):
            for y in range(self.selection.height):
                if(self.selection.selected(x,y)):
                    pixels[(x,y)] = (0,0,0,0)

        foreground.save(self.filename)

        # Free lock to release next thread
        self.lock.release()

    def breakLines(self):
        words = self.text.split()

        carry = words[0] 
        line = 0
        paragraphs = []

        #Watch out, this is a unusual loop, read carefully before updating
        for i in range(1, len(words)):
            carrySize = self.font.getsize(carry)
            #print "carry of: "+carry+" = ("+str(carrySize[0])+","+str(carrySize[1])+")"
            #print str(i) + " - " + str(len(words))
            if  (carrySize[0] > self.size[0]) or ((i+1) >= len(words)) :

                position = (0, line*self.lineHeight)
                par = Paragraph.Paragraph(carry, position)
                paragraphs.append(par)
                carry = words[i]
                line +=1;
            else:
                carry += " " + words[i]
        return paragraphs