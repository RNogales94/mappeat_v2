function get(component, onLoad, baseURI = "/mainRest/api/v1/", handleErrors = false) {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("GET", baseURI + component);
	request.responseType = "json";
	
	if(handleErrors)
		request.onload = onLoad;
	else{
		request.onload = function(){
			if (this.status >= 400)
				alert("Error: " + this.statusText + "\n\n" + this.responseText);
			else
				onLoad.call(this);
		};
	}
	
	request.send();
}

function post(component, onLoad, data, baseURI = "/mainRest/api/v1/", handleErrors = false) {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("POST", baseURI + component);
	request.setRequestHeader("Content-type", "application/json");
	request.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
	
	if(handleErrors)
		request.onload = onLoad;
	else{
		request.onload = function(){
			if (this.status >= 400)
				alert("Error: " + this.statusText + "\n\n" + this.responseText);
			else
				onLoad.call(this);
		};
	}
	
	request.send(JSON.stringify(data));
}
