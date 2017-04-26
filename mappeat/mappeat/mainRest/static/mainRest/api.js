var baseURI = "/mainRest/api/v1/"

function get(component, onLoad) {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("GET", baseURI + component);
	request.responseType = "json";
	request.onload = onLoad;
	request.send();
}

function post(component, onLoad, data) {
	"use strict;"
	let request = new XMLHttpRequest();
	request.open("POST", baseURI + component);
	request.setRequestHeader("Content-type", "application/json");
	request.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
	request.onload = onLoad;
	request.send(JSON.stringify(data));
}
