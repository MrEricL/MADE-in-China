
var submitButton = document.getElementById('submit');
var anewButton = document.getElementById('anew');
var addButton = document.getElementById("add");                               
var removeButton = document.getElementById("remove");                         
var list = document.getElementById("selectable");                             


var selectItem = 8;

var addItem = function(e){
     selectItem += 1;
     var nextElement = document.createElement('LI');
     nextElement.innerHTML = "O";
     list.appendChild(nextElement);
 }

addButton.addEventListener('click', addItem);
  
 var removeItem = function(e){
     list.removeChild(list.lastChild);
     selectItem -= 1;
 }
 
 removeButton.addEventListener('click', removeItem);


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
