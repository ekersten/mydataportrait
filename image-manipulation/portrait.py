from portrait import layer1, layer2, layer3, baseLayer, Croma
from PIL import ImageFont, Image, ImageEnhance
import threading

#portrait
size = (900,900)
fnt = ImageFont.truetype('Verlag Black.otf', 40)
croma = 'img/portrait1.jpg'
value = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ut aliquet est. Sed convallis dignissim justo nec porta. Sed volutpat, purus et efficitur porta, justo dui ornare eros, eget dictum dui massa nec massa. Nunc finibus gravida euismod. Praesent quis dui pellentesque, egestas nibh sit amet, fermentum dolor. Donec viverra pretium elementum. Proin fermentum velit a nibh rutrum feugiat. Aliquam vehicula lorem quis justo pretium egestas. Aliquam erat volutpat. Suspendisse vestibulum tempor dui, ac mollis dolor pellentesque et. Vestibulum pharetra vel mauris eu egestas. Sed at placerat ligula. In hac habitasse platea dictumst. Etiam semper sollicitudin velit et hendrerit. Mauris eu pharetra libero.Aliquam vel tortor nec urna semper aliquam. Etiam at ante blandit, faucibus neque at, eleifend urna. Ut urna odio, tempor non ex nec, tristique volutpat sem. Quisque libero lorem, pulvinar in faucibus non, vulputate ut elit. Phasellus scelerisque lacinia mi, ut euismod felis mollis id. Cras pulvinar massa non ultricies ullamcorper. Mauris orci tellus, malesuada sed pellentesque rhoncus, condimentum sed sem. Praesent nibh felis, sagittis mollis mi id, varius fermentum felis.".upper()
fontColor = (245,242,242,128)
baseFileName = 'layers/base.jpg'
threads = []

#create the selection from the croma
im = Image.open(croma).convert('RGBA')

filename = 'layers/layer1.jpg'
layer1Thread = layer1.layer1Thread('ID1', 'layer1', size, filename,value,fnt,fontColor);
layer1Thread.start();
threads.append(layer1Thread);

baseLayer = baseLayer.baseThread('IDBase', 'base', im.copy(), baseFileName)
baseLayer.start()
threads.append(baseLayer);

#join first 2 layers as I need them before creating the other ones
for t in threads:
    t.join()

cromaColor = (51,156,126)
tolerance = 30

cromaSelection = Croma.selectCroma(im, cromaColor, tolerance);
cromaSelection.invert()

filename = 'layers/layer2.png'
base = Image.open(baseFileName).convert('RGBA')
layer2Thread = layer2.layer2Thread('ID2', 'layer2Thread', base.copy(), cromaSelection, filename);

blackColor = (0,0,0,0)
tolerance = 30

blackSelection = Croma.selectCroma(base, blackColor, tolerance);
filename = 'layers/layer3.png'
fnt3 = ImageFont.truetype('Verlag Black.otf', 14)
fontColor3 = (0,118,190,255)
layer3Thread = layer3.layer3Thread('ID2', 'layer3Thread', base.size, blackSelection, filename, value, fnt3, fontColor3);



layer2Thread.start();
layer3Thread.start();

