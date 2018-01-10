var sunday = document.getElementById("sunstatus")
var monday = document.getElementById("monstatus")
var tuesday = document.getElementById("tuesstatus")
var wednesday = document.getElementById("wedstatus")
var thursday = document.getElementById("thurstatus")
var friday = document.getElementById("fristatus")
var satday = document.getElementById("satstatus")




var checkOC = function(e){
	

	var hoursname = e.target.name.concat("hour")
	var hours = document.getElementById(String(hoursname));

	var status = e.target.options[e.target.selectedIndex].value;
	console.log(hoursname)
		try{
		if (status == "close") hours.setAttribute('hidden','true');
		if (status == "open") hours.removeAttribute("hidden");
	}
	catch(errMsg){
		console.log("Error close the console!!!")
	}
}

sunday.addEventListener("change", checkOC);

monday.addEventListener("change", checkOC);

tuesday.addEventListener("change", checkOC);

wednesday.addEventListener("change", checkOC);

thursday.addEventListener("change", checkOC);

friday.addEventListener("change", checkOC);

satday.addEventListener("change", checkOC);