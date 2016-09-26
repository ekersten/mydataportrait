class Paragraph:
    def __init__(self, text, position):
        self.text = text
        self.position = position

    def __str__(self):
        return "("+str(self.position[0])+","+str(self.position[1])+"):"+self.text