var layer1;
var layer2;
var layer3;
var ctx1;
var ctx2;
var ctx3;
var WIDTH = 900;
var HEIGHT = 900;

//first layer  
var layer1Img = new Image();
layer1Img.src = layer1Src;
var pos1 = [0, 0];

//second layer
var layer2Img = new Image();
layer2Img.src = layer3Src;
var pos2 = [0, 0];

//third layer
var layer3Img = new Image();
layer3Img.src = layer4Src;
var pos4 = [0, 0];

//fourth layer Opacity animation
var layer4Img = new Image();
layer4Img.src = layer2Src;
var op4 = 0;

//fifth layer
var layer5Img = new Image();
layer5Img.src = layer5Src;
var pos5 = [0, 0];

function init() {
    layer1 = document.getElementById("layer1");
    ctx1 = layer1.getContext("2d");
    pos1 = [0, layer1.height]

    layer2 = document.getElementById("layer2");
    ctx2 = layer2.getContext("2d");
    pos2 = [layer2.width, 0]

    layer3 = document.getElementById("layer3");
    ctx3 = layer3.getContext("2d");
    pos3 = [-layer3.width, 0]

    layer4 = document.getElementById("layer4");
    ctx4 = layer4.getContext("2d");
    pos4 = [-layer4.width, 0]

    layer5 = document.getElementById("layer5");
    ctx5 = layer5.getContext("2d");
    pos5 = [0, -layer5.height]

    setInterval(drawAll, 10);
    setTimeout(function(){
        setInterval(drawOp,200);
    }, 5000);
}

function drawAll() {
    draw1();
    draw2();
    draw3();
    draw5();
}

function drawOp(){
    draw4();
}

/*function draw1() {
    ctx1.clearRect(0, 0, WIDTH, HEIGHT);
    ctx1.fillStyle = "#FAF7F8";
    ctx1.beginPath();
    ctx1.rect(0,0,WIDTH,HEIGHT);
    ctx1.closePath();
    ctx1.fill();
    ctx1.fillStyle = "#444444";
    ctx1.beginPath();
    ctx1.arc(x, y, 10, 0, Math.PI*2, true);
    ctx1.closePath();
    ctx1.fill();

    if (x + dx > WIDTH || x + dx < 0)
        dx = -dx;
    if (y + dy > HEIGHT || y + dy < 0)
        dy = -dy;

    x += dx;
    y += dy;
}*/

function draw1() {
    if(pos1[1] > 0){
        ctx1.clearRect(0, 0, WIDTH, HEIGHT);
        ctx1.drawImage(layer1Img, pos1[0], pos1[1], WIDTH, HEIGHT, 0, 0, layer1.width, layer1.height);
        pos1[1] -=1;
    }
}

function draw2() {
    if(pos2[0] > 0){
        ctx2.clearRect(0, 0, WIDTH, HEIGHT);
        ctx2.drawImage(layer2Img, pos2[0], pos2[1], WIDTH, HEIGHT, 0, 0, layer2.width, layer2.height);
        pos2[0] -=1;
    }
}

function draw3() {
    if(pos3[0] < 0){
        ctx3.clearRect(0, 0, WIDTH, HEIGHT);
        ctx3.drawImage(layer3Img, pos3[0], pos3[1], WIDTH, HEIGHT, 0, 0, layer3.width, layer3.height);
        pos3[0] +=1;
    }
}

function draw4() {
    if(op4 < 1.0){
        ctx4.clearRect(0, 0, WIDTH, HEIGHT);
        ctx4.globalAlpha = op4;
        ctx4.drawImage(layer4Img, 0, 0, WIDTH, HEIGHT, 0, 0, layer4.width, layer4.height);
        op4 +=0.1;
    }
}

function draw5() {
    if(pos5[1] < 0){
        ctx5.clearRect(0, 0, WIDTH, HEIGHT);
        ctx5.drawImage(layer5Img, pos5[0], pos5[1], WIDTH, HEIGHT, 0, 0, layer5.width, layer5.height);
        pos5[1] +=1;
    }
}

init();