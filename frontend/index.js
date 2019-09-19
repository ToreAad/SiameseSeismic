var jquery = require("jquery");
window.$ = window.jQuery = jquery; // notice the definition of global variables here
require("jquery-ui-dist/jquery-ui.js");


$(function () {
    $("#datepicker").datepicker();
});


var colorPurple = "#cb3594";
var colorGreen = "#659b41";
var colorYellow = "#ffcf33";
var colorBrown = "#986928";

var curColor = colorPurple;
var clickColor = new Array();



function handleImage(e) {
    var reader = new FileReader();
    reader.onload = function (event) {
        baseImage.pop();
        var img = new Image();
        img.onload = function () {
            baseImage.push(img);
            redraw()
        }
        img.src = event.target.result;
    }
    reader.readAsDataURL(e.target.files[0]);
}

target_canvas = document.getElementById('target-canvas');
target_context = target_canvas.getContext("2d");

canvas = document.getElementById('canvas')
context = document.getElementById('canvas').getContext("2d");

var baseImage = new Array();

$("#button-load-data").mousedown(e => {
    $.ajax({
        type:"GET",
        url: "http://127.0.0.1:5002/api/get",
        dataType: 'application/json;charset=UTF-8',
        headers: {
            'Access-Control-Allow-Origin': '*'
        },
        success: function (data) { 
            data = JSON.parse(data);
            // console.log(data)
            var target_image = new Image();
            target_image.src = data.targetDataURL;
            target_image.onload = function () {
                target_context.drawImage(target_image, 0, 0);
            }
            target_canvas.width = target_image.width;
            target_canvas.height = target_image.height;

            var input_image = new Image();
            input_image.src = data.inputDataURL;
            input_image.onload = function () {
                context.drawImage(input_image, 0, 0);
            }
            baseImage.push(input_image);
            canvas.width = input_image.width;
            canvas.height = input_image.height;
        },
        error: function (data) {
            // SUPER UGLY HACK!!!
            data = JSON.parse(data.responseText);
            // console.log(data)
            var target_image = new Image();
            target_image.src = data.targetDataURL;
            target_image.onload = function () {
                target_canvas.width = target_image.width;
                target_canvas.height = target_image.height;
                target_context.drawImage(target_image, 0, 0);

            }

            var input_image = new Image();
            input_image.src = data.inputDataURL;
            input_image.onload = function () {
                canvas.width = input_image.width;
                canvas.height = input_image.height;
                context.drawImage(input_image, 0, 0);
            }
            baseImage.push(input_image);
        }
    });
});

$("#button-class-1").mousedown(e => {
    curColor = colorGreen;
})

$("#button-class-2").mousedown(e => {
    curColor = colorYellow;
})

$("#button-class-3").mousedown(e => {
    curColor = colorBrown;
})





$('#canvas').mousedown(function (e) {
    var mouseX = e.pageX - this.offsetLeft;
    var mouseY = e.pageY - this.offsetTop;

    paint = true;
    addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
    redraw();
});

$('#canvas').mousemove(function (e) {
    if (paint) {
        addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
        redraw();
    }
});

$('#canvas').mouseup(function (e) {
    paint = false;
});

$('#canvas').mouseleave(function (e) {
    paint = false;
});

function clearArray(A) {
    while (A.length > 0) {
        A.pop();
    }
}

$('#button-clear').mousedown(e => {
    clearArray(clickX);
    clearArray(clickY);
    clearArray(clickDrag);
    clearArray(clickColor)
})

var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint;

function addClick(x, y, dragging) {
    clickX.push(x);
    clickY.push(y);
    clickDrag.push(dragging);
    clickColor.push(curColor);
}


function redraw() {
    context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas

    for (var i = 0; i < baseImage.length; i++) {
        img = baseImage[i];
        canvas.width = img.width;
        canvas.height = img.height;
        context.drawImage(img, 0, 0);
    }

    context.strokeStyle = curColor;
    context.lineJoin = "round";
    context.lineWidth = 75;
    context.lineAlpha = 0.25;

    for (var i = 0; i < clickX.length; i++) {
        context.beginPath();
        if (clickDrag[i] && i) {
            context.moveTo(clickX[i - 1], clickY[i - 1]);
        } else {
            context.moveTo(clickX[i] - 1, clickY[i]);
        }
        context.lineTo(clickX[i], clickY[i]);
        context.closePath();
        context.strokeStyle = clickColor[i];
        context.stroke();
    }
}

$("#button-classify").mousedown(e => {
    var cvs_inputLoaderURL = canvas.toDataURL();
    $.ajax({
        type:"POST",
        url: "http://127.0.0.1:5002/api/post",
        dataType: 'application/json;charset=UTF-8',
        headers: {
            'Access-Control-Allow-Origin': '*'
        },
        data: {inputDataURL: cvs_inputLoaderURL},
        success: function (data) { 
            data = JSON.parse(data);
            // console.log(data)
            var target_interpretation = new Image();
            target_interpretation.src = data.targetDataURL;
            target_interpretation.onload = function () {
                target_context.drawImage(target_interpretation, 0, 0);
            }
        },
        error: function (data) {
            // SUPER UGLY HACK!!!
            data = JSON.parse(data.responseText);
            // console.log(data)
            var target_interpretation = new Image();
            target_interpretation.src = data.targetDataURL;
            target_interpretation.onload = function () {
                target_context.drawImage(target_interpretation, 0, 0);
            }
            // console.log('There was an error');
            // console.log(data);
        }
    });
})