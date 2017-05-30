function get(component, onLoad, baseURI = "/mainRest/api/v1/") {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("GET", baseURI + component);
	request.responseType = "json";
	request.onload = onLoad;
	request.send();
}

function post(component, onLoad, data, baseURI = "/mainRest/api/v1/") {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("POST", baseURI + component);
	request.setRequestHeader("Content-type", "application/json");
	request.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
	request.onload = onLoad;
	request.send(JSON.stringify(data));
}
