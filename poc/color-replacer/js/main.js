var ColorReplacer = {
	tolerance: 40,
	init: function(imgUrl){
		this.canvas = document.getElementById("image");
		this.context = this.canvas.getContext("2d");

		this.image = new Image();
		this.image.src = imgUrl;

		var self = this;
		this.image.onload = function() {
				self.canvas.width = this.width;
				self.canvas.height = this.height;


				self.context.drawImage(self.image, 0, 0);
				self.image.style.display = 'none';
			};

	},
	replace: function() {
		this.tolerance = $("#tolerance").val();
		this.loadColors();
		var pixels = this.context.getImageData(0, 0, this.canvas.width, this.canvas.height);

		//var data = pixels.data;
		var hits = 0;
		for(var i =0; i < pixels.data.length; i+=4){

			var curColor = new Color(pixels.data[i], pixels.data[i+1], pixels.data[i+2], pixels.data[i+3]);

			if( this.fromColor.matches(curColor, this.tolerance)){

				hits += 1;
				pixels.data[i] = this.toColor.red;
				pixels.data[i+1] = this.toColor.green;
				pixels.data[i+2] = this.toColor.blue;
			}
		}

		this.context.clearRect(0,0, this.canvas.width, this.canvas.height);
		this.context.putImageData(pixels, 0, 0);
	},
	loadColors: function(){
		this.fromColor = this.hexToRGB($("#fromInput").val());
		this.toColor = this.hexToRGB($("#toInput").val());
	},
	hexToRGB: function(hexString){
		var hex = parseInt(hexString.substring(1),16);
	    var r = hex >> 16;
	    var g = hex >> 8 & 0xFF;
	    var b = hex & 0xFF;
	    return new Color(r,g,b,255);
	},
	compareColor: function(hue1, hue2){

	}
};

var Color = function(r, g, b, a){
	this.red = r;
	this.green = g;
	this.blue = b;
	this.alpha = a || 255;
}

Color.prototype.matches = function(color, tolerance){
	if(	this.red > (color.red - tolerance) && this.red < (color.red + tolerance) &&
		this.green > (color.green - tolerance) && this.green < (color.green + tolerance) && 
		this.blue > (color.blue - tolerance) && this.blue < (color.blue + tolerance)
		)
		return true;
	return false;
}


$(document).ready(function(){
	$("#imgInput").on('change', function(event){
		
		if(this.files && this.files[0]){
			var reader = new FileReader();

			reader.readAsDataURL(this.files[0]);
			reader.onload = function(e){

				ColorReplacer.init(e.target.result);
			}
		}

	});
	$("#go").on('click', function(){
		ColorReplacer.loadColors();
		ColorReplacer.replace();
	})
});