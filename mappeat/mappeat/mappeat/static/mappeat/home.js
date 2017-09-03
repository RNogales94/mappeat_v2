function register(form){
	if( form.pass.value != form.passRepeated.value ){
		alert("Error: Las contraseñas deben coincidir.");
		return false;
	}

	var valores = Object();
	valores.username = form.username.value;
	valores.email = form.mail.value;
	valores.password = form.pass.value;
  valores.restaurant = form.restaurant.value;

	post("register/", function(){
		form.parentNode.innerHTML = "<h4>Registro completado!</h4><p>Recibirá un correo de verificación de creación de una cuenta. Haga clic en el enlace del correo electrónico para finalizar el proceso de configuración y activar su cuenta.</p><p>Asegúrese de revisar la carpeta de SPAM. En caso de no recibir el mensaje, <a>Reenviar correo</a></p>";
	}, valores, true, "/accounts_api/");

	return false;
}