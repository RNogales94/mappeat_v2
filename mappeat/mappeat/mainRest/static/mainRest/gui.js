function loadApp(){
	document.body.innerHTML = `<header>
		<h3>Mappeat</h3>
		<button>Almacén</button>
		<button>Menú</button>
		<button>TPV</button>
		<button>Informes</button>
		<button>Ajustes</button>
		<button onclick="location.reload()">Salir</button>
	</header>
	<main>
		<p>Aplicación tope guapa.</p>
	</main>`;
}

function register(form){
	if( form.pass.value != form.passRepeated.value ){
		alert("Error: Las contraseñas deben coincidir.");
		return false;
	}
	
	var valores = Object();
	valores.username = form.username.value;
	valores.email = form.mail.value;
	valores.password = form.pass.value;
	
	post("register/", function(){
		form.parentNode.innerHTML = "<p>Registro completado, comprueba tu email.</p>";
	}, valores, true, "/accounts_api/");
	
	return false;
}

function login(form){
	var valores = Object();
	valores.username = form.username.value;
	valores.password = form.pass.value;
	
	post("login/", function(){
		loadApp();
	}, valores, true, "/rest-auth/");
	
	return false;
}
