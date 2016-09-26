from portraitimage.lib import layer1, layer2, layer3, layer4, baseLayer, Selection
from PIL import ImageFont, Image, ImageEnhance
import threading
import os


def onUpload(code, folder):
    print("On upload")
    cromaFile = folder + "/" + code + "/" + code + "_base.jpg"
    im = Image.open(cromaFile).convert('RGBA')

    lock = threading.Lock()
    layerPath = getLayerFilename(code, folder, 0)

    layerThread = createGrayScale(im.copy(),layerPath, lock)
    layerThread.join()
    print("END On upload")

def onRequest(code, folder, text):
    print("On request")
    cromaFile = folder + "/" + code + "/" + code + "_base.jpg"
    im = Image.open(cromaFile).convert('RGBA')

    lock = threading.Lock()
    threads = []
    grayPath = getLayerFilename(code, folder, 0)

    grayLayer = Image.open(grayPath).convert('RGBA')

    filenames = getLayerFilename(code, folder)

    #get croma selection from the original image
    selection = createCromaSelection(im.copy())

    layer1 = createLayer1(lock, grayLayer.size, filenames[1], text, selection)
    threads.append(layer1)
    layer2 = createLayer2(lock, grayLayer.copy(), selection, filenames[2])
    threads.append(layer2)
    layer3 = createLayer3(lock, grayLayer.copy(), selection, filenames[3], text)
    threads.append(layer3)
    layer4 = createLayer4(lock, grayLayer.copy(), selection, filenames[4], text)
    threads.append(layer4)
    layer5 = createLayer5(lock, filenames[5], im.size)
    threads.append(layer5)

    for t in threads:
        t.join()
    print("END On request")

def joinLayers(code, folder):

    filenames = getLayerFilename(code, folder)

    layer1 = Image.open(filenames[1]).convert('RGBA')
    layer2 = Image.open(filenames[2]).convert('RGBA')
    layer3 = Image.open(filenames[3]).convert('RGBA')
    layer4 = Image.open(filenames[4]).convert('RGBA')
    layer5 = Image.open(filenames[5]).convert('RGBA')

    out = Image.alpha_composite(layer2, layer3)
    out = Image.alpha_composite(out, layer4)
    out = Image.alpha_composite(out, layer1)
    out = Image.alpha_composite(out, layer5)

    out.save(filenames[6])


def createCromaSelection(image):
    cromaColor = (75,217,196)
    tolerance = 30

    cromaSelection = Selection.Selection.selectColor(image, cromaColor, tolerance);
    cromaSelection.invert()
    return cromaSelection

def  createGrayScale(image, layerPath, lock):
    layerThread = baseLayer.baseThread('IDBase', lock , image.copy(), layerPath)
    layerThread.start()
    return layerThread

def createLayer1(lock, size, layerPath, text, selection):
    
    fnt = ImageFont.truetype('Verlag Black.otf', 40)
    fontColor = (245,242,242,128)
    lineHeight = 40

    layerThread = layer1.layer1Thread('ID1', lock, size, layerPath, text, fnt, fontColor, lineHeight, selection);
    layerThread.start()
    return layerThread

def createLayer2(lock, baseImage, cromaSelection, layerPath):
    layerThread = layer2.layer2Thread('ID2', lock, baseImage, cromaSelection, layerPath);
    layerThread.start()
    return layerThread

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
    return layerThread

def createLayer4(lock, grayImage, cromaSelection, layerPath, text):
    grayColor = (140,140,140,255)
    tolerance = 70

    graySelection = Selection.Selection.selectColor(grayImage.copy(), grayColor, tolerance)
    graySelection.And(cromaSelection)

    fnt3 = ImageFont.truetype('Verlag Light.otf', 14)
    fontColor3 = (0,118,190,255)
    lineHeight3 = 14
    layerThread = layer3.layer3Thread('ID4', lock, grayImage.size, graySelection, layerPath, text, fnt3, fontColor3,lineHeight3)
    layerThread.start()
    return layerThread

def createLayer5(lock, layerPath, size):
    assetDir = os.path.dirname(os.path.realpath(__file__)) + "/img/"
    files = []
    files.append( assetDir + "headline.png" )
    files.append( assetDir + "wunder_logo.png" )
    outFile = layerPath
    layerThread = layer4.layer4Thread('ID4', lock, files, size, outFile)
    layerThread.start()
    return layerThread

def getDataPortrait(folder, code):
    #print(folder)
    return getLayerFilename(code, folder, 6)

def getLayerFilename(code, folder, index = -1):
    layerFiles = []
    layerFiles.append(folder + "/" +  code + "/" + code + "_gray.png")
    layerFiles.append(folder + "/" +  code + "/" + code + "_l1.png")
    layerFiles.append(folder + "/" +  code + "/" + code + "_l2.png")
    layerFiles.append(folder + "/" +  code + "/" + code + "_l3.png")
    layerFiles.append(folder + "/" +  code + "/" + code + "_l4.png")
    layerFiles.append(folder + "/" +  code + "/" + code + "_l5.png")
    layerFiles.append(folder + "/" +  code + "/" + code + "_def.jpg")
    if(index<0):
        return layerFiles
    else:
        return layerFiles[index]


