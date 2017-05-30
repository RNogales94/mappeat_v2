function get(component, onLoad, handleErrors = false, baseURI = "/mainRest/api/v1/") {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("GET", baseURI + component);
	request.responseType = "json";
	
	request.onload = function(){
		if (this.status >= 400 && !handleErrors)
			alert("Error: " + this.statusText + "\n\n" + this.responseText);
		else
			onLoad.call(this);
	};
	
	request.send();
}

function post(component, onLoad, data, handleErrors = false, baseURI = "/mainRest/api/v1/") {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("POST", baseURI + component);
	request.setRequestHeader("Content-type", "application/json");
	request.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
	
	request.onload = function(){
		if (this.status >= 400 && !handleErrors)
			alert("Error: " + this.statusText + "\n\n" + this.responseText);
		else
			onLoad.call(this);
	};
	
	request.send(JSON.stringify(data));
}
