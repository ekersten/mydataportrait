#Provides support to mapping a selection on an image
class Selection:
	positions = []
	width = 0;
	height = 0;

	def __init__(self, width, height):
		self.width = width
		self.height = height
		for x in range(width):
			self.positions.append([])

	def select(self, pixels, criteria):
		for x in range(self.width):
			for y in range(self.height):
				self.positions[x].append(criteria.select(pixels[x,y]))

	def invert(self):
		for x in range(self.width):
			for y in range(self.height):
				self.positions[x][y] = not self.positions[x][y]

	def selected(self,x,y):
		return self.positions[x][y]

	def first(self):
		for x in range(self.width):
			for y in range(self.height):
				if(self.positions[x][y]):
					return (x,y)
					
	def Or(self,selction):
		for x in range(self.width):
			for y in range(self.height):
				if(self.positions[x][y]):
					return (x,y)