var sunday = document.getElementByName("sunstatus")


var checkOC = function(){
	var sundayStatus = sunday.options[sunday.selectedIndex].text;
	console.log("closed");
	if (sundayStatus == "close") this.remove();
}

sunday.addEventListener("change", checkOC);