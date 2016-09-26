#Provides support to mapping a selection on an image
class Selection:
    def __init__(self, width, height):
        self.positions = []
        self.width = width
        self.height = height
        self.debug = []
        for x in range(width):
            self.positions.append([])


    def select(self, pixels, criteria):
        for x in range(self.width):
            for y in range(self.height):
                #if x == 0:
                    #print("", end="\n")
                self.positions[x].append(criteria.select(pixels[x,y]))

    def invert(self):
        for x in range(self.width):
            for y in range(self.height):
                self.positions[x][y] = not self.positions[x][y]

    def selected(self,x,y):
        return self.positions[x][y]

    def first(self):
        minX = self.width
        minY = self.height
        for x in range(self.width):
            for y in range(self.height):
                if(self.positions[x][y]):
                    if x < minX:
                        minX = x
                    if y < minY:
                        minY = y
        return ( minX, minY)

    def Or(self,selction):
        for x in range(self.width):
            for y in range(self.height):
                if(selection.selected(x,y) or self.selected(x,y)):
                    self.positions[x][y] = True
                else:
                    self.positions[x][y] = False

    def And(self,selection):
        count = 0
        for x in range(self.width):
            for y in range(self.height):
                if(selection.selected(x,y) and self.selected(x,y)):
                    self.positions[x][y] = True
                    count +=1
                else:
                    self.positions[x][y] = False
        #print("Selected "+str(count)+" pixels")


    @staticmethod
    def selectColor(im, color, tolerance):
        selector = ColorSelector(color, tolerance)
        pixels = im.load()
        selection = Selection(im.width, im.height)
        #print("Selection color: ("+str(color[0])+","+str(color[1])+","+str(color[2])+") with tolerance "+str(tolerance),end="\n")
        selection.select(pixels, selector)
        #print("Selection color: ("+str(color[0])+","+str(color[1])+","+str(color[2])+") with tolerance "+str(tolerance),end="\n")
        return selection

class ColorSelector:
    def __init__(self, color, tolerance):
        self.color = color
        self.tolerance = tolerance

    def select(self, pixel):
        if( (self.color[0] - self.tolerance) <= pixel[0] <= (self.color[0] + self.tolerance) and 
            (self.color[1] - self.tolerance) <= pixel[1] <= (self.color[1] + self.tolerance) and 
            (self.color[2] - self.tolerance) <= pixel[2] <= (self.color[2] + self.tolerance)
        ):
            #print("1",end="")
            return True
        #print("0",end="")
        return False




