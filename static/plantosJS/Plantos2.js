// File:src/Plantos.js
/**
 * @author Logan Martin
 * Revision 2 starts use with Unity
 * Most functions that previously existed in Plantos 
 * 	now exist in the Unity project files
 * 	To view Unity project files, visit CityFarm on github
 *		GitHub > MIT-CityFARM > plantos-server > Untiy Project Files
 * 
 */


var Plantos = { REVISION: '2' };
// browser support
if ( typeof module === 'object' ) {
	module.exports = Plantos;
}
// polyfills
if ( Math.sign === undefined ) {
	// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/sign
	Math.sign = function ( x ) {
		return ( x < 0 ) ? - 1 : ( x > 0 ) ? 1 : +x;
	};
}

// set the default log handlers
Plantos.log = function() { console.log.apply( console, arguments ); }
Plantos.warn = function() { console.warn.apply( console, arguments ); }
Plantos.error = function() { console.error.apply( console, arguments ); }

/* Debug Settings */
Plantos.debug = {
	resize: true,
};
//var aspect = 1.6;
/* Plantos Functions */

/* General Functions */
function resizeCanvas() {
	var width = 0.9*window.innerWidth;
	var height = 0.9*window.innerHeight;
	var canvasMargin = 5;
	if(height*aspect < width){
		width = height*aspect;
	}
	if(width/aspect < height){
		height = width/aspect;
	}
	if(Plantos.debug.resize){
		console.log("Resize event \n-New Width: " + width + "\n-New Height: " + height);
	}
	if (canvas.width != width || canvas.height != height) {
		// Change the size of the canvas to match the size it's being displayed
		canvas.width = width-canvasMargin;
		canvas.height = height-canvasMargin;
	}
};




/* Event Listeners */
window.addEventListener('resize', resizeCanvas);







