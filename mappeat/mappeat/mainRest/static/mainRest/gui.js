var main;
var familyWanted;

function loadFamily(name){
	familyWanted = name;
	document.getElementById('productsList').innerHTML = "Cargando...";

	get("products/?family=" + name, function(){
			"use strict";
			if (familyWanted == name){
				let list = document.getElementById('productsList');
				list.innerHTML = '';

				for (let product of this.response){
					list.insertAdjacentHTML('beforeend', `<li onclick="void(0)">${product.name}</li>`);
				}
			}
	});
}

function loadTPV(){
	main.innerHTML = `<div class="container-fluid">
	  <div class="row content">
		 <div class="col-sm-1 sidenav " style="width: 12%">
		     <div class="btn-group-vertical" style="width: 110%">
		     <button type="button" class="btn btn-primary">Ver Mesas</button>
		     <button type="button" class="btn btn-warning" >Abrir Cajón</button>
		     <button type="button" class="btn btn-success">Efectivo <span class="badge"> 12.50€</span></button>
		     <button type="button" class="btn btn-success">Cobro Avanzado</button>
		     <button type="button" class="btn btn-primary">Dividir Ticket</button>
		     <button type="button" class="btn btn-basic">Enviar a Cocina</button>
		     <button type="button" class="btn btn-danger">Borrar Linea</button>
		     <button type="button" class="btn btn-info">Añadir Nota</button>
		     <button type="button" class="btn btn-warning">Transferir Mesa</button>
		     <button type="button" class="btn btn-primary">Buscar Ticket</button>
		     <button type="button" class="btn btn-info">Imprimir Ticket</button>
		     <button type="button" class="btn btn-danger">Cancelar Ticket</button>
		     </div><br>
		 </div>
		 <br>

		 <div class="col-sm-10">
		   <div class="row">
		     <div class="col-sm-8">
		       <div class="well">
		         <h4>Familias</h4>
		         <ul id="familiesList">Cargando...</ul>
		       </div>
		     </div>
		     <div class="col-sm-4">
		       <div class="well">
		         <h4>Contexto Actual</h4>
		         <p>Total cuenta</p>
		         <p>Nombre Camarero</p>
		         <p>Numero de Mesa</p>
		         <p>Numero de Ticket</p>
		       </div>
		     </div>
		   </div>
		   <div class="row">
		     <div class="col-sm-8">
		       <div class="well">
		         <h4>Productos</h4>
		         <ul id="productsList">Cargando...</ul>
		       </div>
		         <div class="well">
		         <h4> Sugerencias de productos </h4>
		         <p> Aqui aparece una lista de productos de varias familias que tienen una gran probabilidad de ser incluídos en el ticket</p>
		       </div>
		     </div>
		     <div class="col-sm-4">
		       <div class="well">
		         <h4>Ticket Actual</h4>
		         <p>Contiene una lista dinámica con todos los productos del ticket actual</p>
		       </div>
		     </div>
		   </div>
		 </div>
	  </div>
	</div>`;

	familyWanted = '';

	get("families/", function(){
			"use strict";
			let list = document.getElementById('familiesList');
			list.innerHTML = '';

			for (let family of this.response){
				list.insertAdjacentHTML('beforeend', `<li onclick="loadFamily('${encodeURIComponent(family.name)}')">${family.name}</li>`);
			}
	});

	get("products/", function(){
			"use strict";
			if (familyWanted == ''){
				let list = document.getElementById('productsList');
				list.innerHTML = '';

				for (let product of this.response){
					list.insertAdjacentHTML('beforeend', `<li onclick="void(0)">${product.name}</li>`);
				}
			}
	});
}

function loadApp(){
	document.body.innerHTML = `<header>
		<h2>Mappeat</h2>
		<button>Almacén</button>
		<button>Menú</button>
		<button onclick="loadTPV()">TPV</button>
		<button>Informes</button>
		<button>Ajustes</button>
		<button onclick="location.reload()">Salir</button>
	</header>
	<main>
	</main>`;

	main = document.querySelector('main');
	loadTPV();
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
