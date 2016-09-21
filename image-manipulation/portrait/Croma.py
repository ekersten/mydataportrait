import Selection

def selectCroma(im, color, tolerance):
	selector = ColorSelector(color, tolerance)
	pixels = im.load()
	selection = Selection.Selection(im.width, im.height)
	selection.select(pixels, selector)
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
			return True
		return False