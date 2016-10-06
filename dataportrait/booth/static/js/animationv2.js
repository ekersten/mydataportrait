var layer1;
var layer2;
var layer3;
var ctx1;
var ctx2;
var ctx3;
var WIDTH = 900;
var HEIGHT = 900;
var MAXSCREENWIDTH = 900;
var padding = 20;
var layerCount = 5;
var loadedImages = 0;

//first layer  
var layer1Img = new Image();
layer1Img.onload = synchedInit;
layer1Img.src = layer1Src;
var pos1 = [0, 0];

//second layer
var layer2Img = new Image();
layer1Img.onload = synchedInit;
layer2Img.src = layer3Src;
var pos2 = [0, 0];

//third layer
var layer3Img = new Image();
layer1Img.onload = synchedInit;
layer3Img.src = layer4Src;
var pos4 = [0, 0];

//fourth layer Opacity animation
var layer4Img = new Image();
layer1Img.onload = synchedInit;
layer4Img.src = layer2Src;
var op4 = 0;

//fifth layer
var layer5Img = new Image();
layer1Img.onload = synchedInit;
layer5Img.src = layer5Src;
var op5 = 0;


function synchedInit(){
    if(loadedImages >= layerCount){
        init();
    }
    loadedImages +=1;
}

function init() {
    layer1 = document.getElementById("layer1");
    ctx1 = layer1.getContext("2d");    

    layer2 = document.getElementById("layer2");
    ctx2 = layer2.getContext("2d");

    layer3 = document.getElementById("layer3");
    ctx3 = layer3.getContext("2d");

    layer4 = document.getElementById("layer4");
    ctx4 = layer4.getContext("2d");

    layer5 = document.getElementById("layer5");
    ctx5 = layer5.getContext("2d");

    /* image is always square */
    if(window.innerWidth < MAXSCREENWIDTH){
        var w = window.innerWidth -20;
        layer1.width = w;
        layer1.height = w;

        layer2.width = w;
        layer2.height = w;

        layer3.width = w;
        layer3.height = w;

        layer4.width = w;
        layer4.height = w;

        layer5.width = w;
        layer5.height = w;
    }else{
        layer1.width = MAXSCREENWIDTH;
        layer1.height = MAXSCREENWIDTH;

        layer2.width = MAXSCREENWIDTH;
        layer2.height = MAXSCREENWIDTH;

        layer3.width = MAXSCREENWIDTH;
        layer3.height = MAXSCREENWIDTH;

        layer4.width = MAXSCREENWIDTH;
        layer4.height = MAXSCREENWIDTH;

        layer5.width = MAXSCREENWIDTH;
        layer5.height = MAXSCREENWIDTH;
    }

    pos1 = [0, layer1.height];
    pos2 = [0, -layer2.height];
    pos3 = [0, -layer3.height];

    setInterval(drawAll, 10);
    setTimeout(function(){
        setInterval(drawOp,200);
    }, 5000);
}

function drawAll() {
    draw1();
    draw2();
    draw3();
}

function drawOp(){
    draw5();
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
    if(pos2[1] < 0){
        ctx2.clearRect(0, 0, WIDTH, HEIGHT);
        ctx2.drawImage(layer2Img, pos2[0], pos2[1], WIDTH, HEIGHT, 0, 0, layer2.width, layer2.height);
        pos2[1] +=1;
    }
}

function draw3() {
    if(pos3[1] < 0){
        ctx3.clearRect(0, 0, WIDTH, HEIGHT);
        ctx3.drawImage(layer3Img, pos3[0], pos3[1], WIDTH, HEIGHT, 0, 0, layer3.width, layer3.height);
        pos3[1] +=1;
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
    if(op5 < 1.0){
        ctx5.clearRect(0, 0, WIDTH, HEIGHT);
        ctx5.globalAlpha = op5;
        ctx5.drawImage(layer5Img, 0, 0, WIDTH, HEIGHT, 0, 0, layer1.width, layer1.height);
        op5 +=0.1;
    }
}

init();