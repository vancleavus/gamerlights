function submitColor(event) {
    const staticColor = document.getElementById("sColor").value;
    const fadeColor1 = document.getElementById("fColor1").value;
    const fadeColor2 = document.getElementById("fColor2").value;
    const mode = event.target.id;
    
    const data = {  'requestType' : 'submit',
                    'staticColor' : staticColor,
                    'fadeColor1' : fadeColor1,
                    'fadeColor2' : fadeColor2,
                    'mode' : mode,
                    'timestamp' : Date.now()}; 
    
    fetch("gamerlights_source/gamerlights_ajax_backend.php", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {'content-type': 'application/json'}
    })
    .then(response => response.json())
    .then(data => receiveColorData(data))
    .catch(err => console.log(err))
    
}

function fetchColorData(event){
    const data = { 'requestType' : "fetch"};
    fetch("gamerlights_source/gamerlights_ajax_backend.php", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {'content-type': 'application/json'}
    })
    .then(response => response.json())
    .then(data => receiveColorData(data))
    .catch(err => console.log(err))
}

function receiveColorData(data){
    //given data from gamerlights_ajax_backend.php, update color canvas thing and input colors too
    document.getElementById("sColor").value=data.staticColor;
    document.getElementById("fColor1").value=data.fadeColor1;
    document.getElementById("fColor2").value=data.fadeColor2;
    if(data.mode == "static") {
        document.getElementById("colorCanvas").style = `background-color: ${data.staticColor}`;
    } else if (data.mode == "fade") {
        document.getElementById("colorCanvas").style = `background-image: linear-gradient(${data.fadeColor1}, ${data.fadeColor2}`;
    } else if (data.mode == "rainbow") {
        document.getElementById("colorCanvas").style = `background-image: linear-gradient(magenta, red, yellow, green, cyan, blue, purple)`;
    } else if(data.mode == "off") {
        document.getElementById("colorCanvas").style = `background-color: black`;
    } else {
        document.getElementById("colorCanvas").style = `display: none`;
    }
}

function resetDefaultColors(event) {
    document.getElementById("sColor").value="#a00040";
    document.getElementById("fColor1").value="#d00010";
    document.getElementById("fColor2").value="#4020a0";
}

document.getElementById("static").addEventListener("click", submitColor, false);
document.getElementById("fade").addEventListener("click", submitColor, false);
document.getElementById("rainbow").addEventListener("click", submitColor, false);
document.getElementById("off").addEventListener("click", submitColor, false);
document.getElementById("reset").addEventListener("click", resetDefaultColors, false);

document.addEventListener("DOMContentLoaded", fetchColorData, false);
