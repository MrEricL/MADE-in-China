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
