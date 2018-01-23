var alertable = true;

var all = document.getElementById("everything");

var submitButton = document.getElementById('submit');
var anewButton = document.getElementById('anew');
//var addButton = document.getElementById("add");                               
//var removeButton = document.getElementById("remove");                         
var list = document.getElementById("selectable");                             

var m = document.getElementById("m");
var mButton = document.getElementById("mButton");

var n = document.getElementById("n");
//var nButton = document.getElementById("nButton");       

var selectItem = 8;

/*var addItem = function(e){
     selectItem += 1;
     var nextElement = document.createElement('LI');
     nextElement.innerHTML = "O";
     list.appendChild(nextElement);
 }

 addButton.addEventListener('click', addItem);*/

var addMN = function(e){
    for(j = 0; j < n.value; j++){
        for(i = -1; i < m.value; i++){
            selectItem += 1;
            var nextElement = document.createElement('LI');
            nextElement.innerHTML = " ";
            nextElement.className = "ui-widget-content";
            //nextElement.style.background = "green";                             
            nextElement.style.border = "green";
            if(i == (m.value - 1)){
                nextElement.style.marginLeft = "1200px";
                nextElement.style.backgroundColor = "white";
                nextElement.style.height = "0px";
                nextElement.style.width = "0px";
                nextElement.style.marginTop = "0px";
                nextElement.style.marginBottom = "0px";
            }


            list.appendChild(nextElement);

        }
    }
    var finalElement = document.createElement('LI');
    finalElement.innerHTML = "Start selecting tables?";
    finalElement.style.width = "1200px";
    finalElement.style.backgroundColor = "green";
    list.appendChild(finalElement);
}

var mDisable = function(e){

    if(((m.value > 7) || (n.value > 7)) || ((m.value < 1) || (n.value < 1))){
        mButton.disabled = true;
        if(alertable == true){
            window.alert("7x7 is the largest possible size");
        }
        alertable = false;
    }
    else{
        mButton.disabled = false;
        alertable = true;
    }
}

all.addEventListener('mouseover', mDisable);

mButton.addEventListener('click', addMN);
  
/* var removeItem = function(e){
     list.removeChild(list.lastChild);
     selectItem -= 1;
 }
 
 removeButton.addEventListener('click', removeItem);*/


var submit = function(e){
    $("#selectable").selectable("destroy");
}

var anew = function(e){
    document.location.reload();
}

anewButton.addEventListener("click", anew);


//NEW STUFF

var fin = document.getElementById("finalize");

var createCanv = function(e){
	    html2canvas(document.getElementById("target"), {
        onrendered: function (canvas) {
            var dataURL = canvas.toDataURL();
            var ret  = document.createElement("input")
            ret.setAttribute("type", "hidden");
            ret.setAttribute("name", "pic");
            ret.setAttribute("value", dataURL)
            console.log(ret)
            /*console.log(retdataURL);*/
            document.getElementById('target').appendChild(ret);
        }
    });

}

fin.addEventListener('click',createCanv)
