function get(component, onLoad, handleErrors = true, baseURI = "/mainRest/api/v1/",cors=true) {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("GET", baseURI + component);
	request.responseType = "json";
    if(cors){
	request.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
    }
	request.onload = function(){
		if (this.status >= 400 && handleErrors)
			alert("Error: " + this.statusText + "\n\n" + this.responseText);
		else
			onLoad.call(this);
	};
	
	request.send();
}

function post(component, onLoad, data, handleErrors = true, baseURI = "/mainRest/api/v1/") {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("POST", baseURI + component);
	request.responseType = "json";
	request.setRequestHeader("Content-type", "application/json");
	request.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
	
	request.onload = function(){
		if (this.status >= 400 && handleErrors)
			alert("Error: " + this.statusText + "\n\n" + this.responseText);
		else
			onLoad.call(this);
	};
	
	request.send(JSON.stringify(data));
}

function put(component, onLoad,data, handleErrors = true, baseURI = "/mainRest/api/v1/") {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("PUT", baseURI + component);
	request.responseType = "json";
	request.setRequestHeader("Content-type", "application/json");
	request.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
	
	request.onload = function(){
		if (this.status >= 400 && handleErrors)
			alert("Error: " + this.statusText + "\n\n" + this.responseText);
		else
			onLoad.call(this);
	};
	
	request.send(JSON.stringify(data));
}

function _delete(component, onLoad, data, handleErrors = true, baseURI = "/mainRest/api/v1/") {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("DELETE", baseURI + component);
	request.responseType = "json";
	request.setRequestHeader("Content-type", "application/json");
	request.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
	
	request.onload = function(){
		if (this.status >= 400 && handleErrors)
			alert("Error: " + this.statusText + "\n\n" + this.responseText);
		else
			onLoad.call(this);
	};
	
	request.send(JSON.stringify(data));
}
