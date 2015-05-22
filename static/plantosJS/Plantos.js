// File:src/Plantos.js
/**
 * @author Logan Martin
 */
var Plantos = { REVISION: '1' };
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

/* Variables */

//var clickable = {};
Plantos.recursiveCounter = 0;
Plantos.OpacityFactor = 5.0;
//var scene, camera, renderer, light;
var container = {};
var setupVars = {
	camFOV:60,
	camNear:0.1,
	camFar:30,
	camRot:{
		x:-0.3,
		y:0,
		z:0,
	},
	lightColor:0xffffff,
	lightIntensity:1.0,
	lightPos:{
		x:15,
		y:17.5,
		z:15.5,
	},
	lightRot:{
		x:-0.35,
		y:0,
		z:0,
	},
	rendBGColor:0x005500,
	rendBGOpacity:0.25,
};
var PlantosRoot;
//Objects

//Nodes
Plantos.Node = function(node){
	return this.setNode(node);
};
Plantos.Node.prototype = {
	constructor: Plantos.Node,
	node:{},
	setNode: function(node){
		this.node = node;
	}
};

//Plantos Functions
Plantos.setupCanvas = function(){
	scene = new THREE.Scene();
	camera = new THREE.PerspectiveCamera(
			setupVars.camFOV, 
			container.aspectRatio,
			setupVars.camNear,
			setupVars.camFar);
	light = new THREE.DirectionalLight(
			setupVars.lightColor,
			setupVars.lightIntensity);
	renderer = new THREE.WebGLRenderer({alpha:true});
	renderer.setSize(container.width, container.height);
	renderer.setClearColor(setupVars.rendBGColor, setupVars.rendBGOpacity);

	container.$canvas.append(renderer.domElement);
	scene.add(light);

	camera.rotation.set(setupVars.camRot.x, setupVars.camRot.y, setupVars.camRot.z);
	light.position.set(setupVars.lightPos.x, setupVars.lightPos.y, setupVars.lightPos.z);
	light.rotation.set(setupVars.lightRot.x, setupVars.lightRot.y, setupVars.lightRot.z);
}
/**
 * Moves the items of list a to list b
 * @param a must be instance of THREE.Object3D with some children
 * @param b must be instance of THREE.Object3D
 */
Plantos.moveList = function(a, b){
	var numChildren = a.children.length;
	for(var i=0; i<numChildren; i++){
		b.add(a.children[0]);
	}
}
/**
 * Adds the children of a specified node to a list
 * @param list, must be instance of THREE.Object3D
 * @param node, iobject with children
 */
Plantos.addChildren = function(list, node){
	//for (var c in node.children){
	//	clickable.add(node.children[c].obj);
	//}
	
	if( ! ( node.hasOwnProperty( "children" ) ) ) {
		return
	}
	node.children.forEach(function(child){
		list.add(child.obj);
	});
}
/**
 * Updates the root node by setting the designated root to the 
 *	new node, and sets clickable to the children of the new node
 */
Plantos.updateRootNode = function(root, newNode, clickList, otherList){

	if(!clickList) clickList = clickable;
	if(!otherList) otherList = structureList;
	root.setNode(newNode);
	//moveCameraToObject(camera, root.node.obj);
	Plantos.moveList(clickList, otherList);
	Plantos.addChildren(clickList, newNode);
}
Plantos.relMouseCoords = function(event){
    var totalOffsetX = 0;
    var totalOffsetY = 0;
    var canvasX = 0;
    var canvasY = 0;
    var currentElement = this;

    do{
        totalOffsetX += currentElement.offsetLeft - currentElement.scrollLeft;
        totalOffsetY += currentElement.offsetTop - currentElement.scrollTop;
    }
    while(currentElement = currentElement.offsetParent)

    canvasX = event.clientX - totalOffsetX;
    canvasY = event.clientY - totalOffsetY;

    return {x:canvasX, y:canvasY}
}

Plantos.setOpacity = function(node, factor){
	var obj = node.obj;
	if(!("children" in node) && !("plant" in node)){
		return
	}
	if(!(obj instanceof THREE.Mesh)){ //collada object
		obj.meshes.forEach( function(box){
			box.material.transparent = true;
			box.material.opacity *=factor;
		} );
	}
	else if(obj instanceof THREE.Mesh){
		obj.material.transparent = true;
		obj.material.opacity *=factor;
	}
	
	
}




//General Functions
function findMeshes(obj, list){
	if(obj instanceof THREE.Mesh){
		list.push(obj);
	}else{
		if("children" in obj ){
			obj.children.forEach(function(child){
				findMeshes(child, list);
			});
		}else{
			return;
		}
	}
}
function onMouseMove( event ) {
	var canvas = renderer.domElement;
	var relMouse = canvas.relMouseCoords(event);
	var offset = $('#canvas').offset();
	mouse.x = ( (relMouse.x) / canvas.width ) * 2 - 1;
	mouse.y = - ( (relMouse.y) / canvas.height ) * 2 + 1;
	mouse.z = 0.5;//camera.position.z;			
}
function onWindowResize(){
    //camera.aspect = $cont.width()/;
    container.width = container.$canvas.width();
	container.height = container.width*1.0/container.aspectRatio;
    camera.updateProjectionMatrix();
    renderer.setSize( container.width, container.height );
}
HTMLCanvasElement.prototype.relMouseCoords = Plantos.relMouseCoords;
function relMouseCoords(event){
    var totalOffsetX = 0;
    var totalOffsetY = 0;
    var canvasX = 0;
    var canvasY = 0;
    var currentElement = this;

    do{
        totalOffsetX += currentElement.offsetLeft - currentElement.scrollLeft;
        totalOffsetY += currentElement.offsetTop - currentElement.scrollTop;
    }
    while(currentElement = currentElement.offsetParent)

    canvasX = event.clientX - totalOffsetX;
    canvasY = event.clientY - totalOffsetY;

    return {x:canvasX, y:canvasY}
}

function setColor(obj, color){
	if(obj instanceof THREE.Group){ //collada object
		obj.children[0].children.forEach( function(box){
			box.material.color = color;
		} );
	}
	else if(obj instanceof THREE.Mesh){
		obj.material.color = color;
	}
}
/** 
 * Recursively draws the structure tree using three.js and some jQuery
 * @param tree A system tree from the CityFarm plantos API
 * @param items the three.js Object3D the top node will be added to
 * @param parentPos *optional* a 3-element list of ints for the position of the parent. 
 * 		Default value is [0,0,0]
 */
function drawTree(node, items, parentPos, parent){
	
	parentPos = parentPos || [0,0,0];
	var childBool = ("children" in node);
	var obj, mat;
	if(node.model != null){ //Use 3d model (must be collada file)
		//return;
		
		var loader = new THREE.ColladaLoader();
		loader.options.convertUpAxis = true;
		var model = node.model;
		//console.log(model);
		//console.log(model.file);
		//console.log(node.model.file);
		loader.load(model.file, loadObj);
		function loadObj(coll){
			
			var matColor = 0xdd0000;
			mat = new THREE.MeshLambertMaterial({color:matColor});
			obj = coll.scene;
			//Set position
			if(!("x" in node)){
				node.x=0;
				node.y=0;
				node.z=0;
			}

			obj.position.set(
				parentPos[0]+node.x,
				parentPos[2]+node.z,
				parentPos[1]+node.y+node.width
			);
			//Scale to correct size
			obj.scale.x = obj.scale.x*(node.length/model.length);
			obj.scale.y = obj.scale.y*(node.height/model.height);
			obj.scale.z = obj.scale.z*(node.width/model.width);

			//get all meshes in an object
			obj.meshes = [];
			findMeshes(obj, obj.meshes);

			//set object porperties
			obj.node = node;
			obj.meshes.forEach(function(mesh){
				mesh.originalColor = mesh.material.color;
				mesh.node = node;
			} );

			//set node object
			node.obj = obj;
			//console.log(obj);
			node.parent = parent;
			items.add(obj);

			if (childBool){
				var myPos = [node.x+parentPos[0], node.y+parentPos[1], node.z+parentPos[2]]
				for (var child in node.children){
					Plantos.recursiveCounter+=1;
					drawTree(node.children[child], items, myPos, node );
				}
			}
			Plantos.recursiveCounter--;
			if(Plantos.recursiveCounter == 0){
				start();
			}
		}
	}
	else{ //If no 3d model is provided - Uses boxes and wireframes
		var geo, mat;
		var matColor = 0x00bb00;
		geo = new THREE.BoxGeometry(node.length, node.height, node.width);
		if('children' in node){
			matColor = 0x007700;
			mat = new THREE.MeshBasicMaterial({color:matColor, wireframe:true});
		}
		else{
			mat = new THREE.MeshLambertMaterial({color:matColor});
		}
		obj = new THREE.Mesh(geo, mat);

		obj.position.set(
			node.x + node.length/2 + parentPos[0],
			node.z + node.height/2 + parentPos[2],
			node.y + node.width /2 + parentPos[1]
		);
		obj.originalColor = mat.color;
		obj.node = node
		node.obj = obj;
		node.parent = parent;
		items.add(obj);
		if (childBool){
			var myPos = [node.x, node.y, node.z]
			for (var child in node.children){
				Plantos.recursiveCounter+=1;
				drawTree(node.children[child], items, myPos, node );
			}
		}
		Plantos.recursiveCounter--;
		if(Plantos.recursiveCounter == 0){		
			start();
		}
	}
}





