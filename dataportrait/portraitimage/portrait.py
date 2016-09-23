from lib import layer1, layer2, layer3, baseLayer, Croma, Selection
from PIL import ImageFont, Image, ImageEnhance
import threading


def onUpload(code, folder):
	cromaFile = folder + "/" + code + ".jpg"
	im = Image.open(cromaFile).convert('RGBA')

	lock = threading.Lock()
	layerPath = getLayerFilename(code, folder, 0)

	createGrayScale(im.copy(),layerPath, lock)

def onRequest(code, folder, text):

	cromaFile = folder + "/" + code + ".jpg"
	im = Image.open(cromaFile).convert('RGBA')

	lock = threading.Lock()
	grayPath = folder + code + "_gray.png"

	grayLayer = Image.open(grayPath).convert('RGBA')

	filenames = getLayerFilename(code, folder)

	#get croma selection from the original image
	selection = createCromaSelection(im.copy())

	createLayer1(lock, grayLayer.size, filenames[1], text, selection)
	createLayer2(lock, grayLayer, selection, filenames[2])
	createLayer3(lock, grayLayer, selection, filenames[3], text)
	createLayer4(lock, grayLayer, selection, filenames[4], text)

def joinLayers(code, folder):

	filenames = getLayerFilename(code, folder)

	layer1 = Image.open(filenames[1]).convert('RGBA')
	layer2 = Image.open(filenames[2]).convert('RGBA')
	layer3 = Image.open(filenames[3]).convert('RGBA')
	layer4 = Image.open(filenames[4]).convert('RGBA')

	out = Image.alpha_composite(layer2, layer3)
	out = Image.alpha_composite(out, layer4)
	out = Image.alpha_composite(out, layer1)

	out.save(filenames[5])


def createCromaSelection(image):
	cromaColor = (51,156,126)
	tolerance = 30

	cromaSelection = Selection.Selection.selectColor(image, cromaColor, tolerance);
	cromaSelection.invert()
	return cromaSelection

def  createGrayScale(image, layerPath, lock):
	layerThread = baseLayer.baseThread('IDBase', lock , image.copy(), layerPath)
	layerThread.start()

def createLayer1(lock, size, layerPath, text, selection):
	
	fnt = ImageFont.truetype('Verlag Black.otf', 40)
	fontColor = (245,242,242,128)
	lineHeight = 40

	layerThread = layer1.layer1Thread('ID1', lock, size, layerPath, text, fnt, fontColor, lineHeight, selection);
	layerThread.start()

def createLayer2(lock, baseImage, cromaSelection, layerPath):
	layerThread = layer2.layer2Thread('ID2', lock, baseImage, cromaSelection, layerPath);
	layerThread.start()

def createLayer3(lock, grayImage, cromaSelection, layerPath, text):
	blackColor = (0,0,0,0)
	tolerance = 70

	blackSelection = Selection.Selection.selectColor(grayImage.copy(), blackColor, tolerance)
	blackSelection.And(cromaSelection)

	fnt3 = ImageFont.truetype('Verlag Black.otf', 14)
	fontColor3 = (0,118,190,255)
	lineHeight3 = 14
	layerThread = layer3.layer3Thread('ID3', lock, grayImage.size, blackSelection, layerPath, text, fnt3, fontColor3,lineHeight3)
	layerThread.start()	

def createLayer4(lock, grayImage, cromaSelection, layerPath, text):
	grayColor = (120,120,120,120)
	tolerance = 50

	graySelection = Selection.Selection.selectColor(grayImage.copy(), grayColor, tolerance)
	graySelection.And(cromaSelection)

	fnt3 = ImageFont.truetype('Verlag Light.otf', 14)
	fontColor3 = (0,118,190,255)
	lineHeight3 = 14
	layerThread = layer3.layer3Thread('ID4', lock, grayImage.size, graySelection, layerPath, text, fnt3, fontColor3,lineHeight3)
	layerThread.start()

def getLayerFilename(code, folder, index = -1):
	layerFiles = []
	layerFiles.append(folder + code + "_gray.png")
	layerFiles.append(folder + code + "_l1.png")
	layerFiles.append(folder + code + "_l2.png")
	layerFiles.append(folder + code + "_l3.png")
	layerFiles.append(folder + code + "_l4.png")
	layerFiles.append(folder + code + "_def.jpg")
	if(index<0):
		return layerFiles
	else:
		return layerFiles[index]


