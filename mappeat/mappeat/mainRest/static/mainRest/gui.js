var main;
var familyWanted;
var currentTable;
var currentTableID;

function loadSettings(){
	main.innerHTML = `<div class="container-fluid">
                            <div class="col-sm-1 sidenav " style="width: 12%">
		                      <h3>Ajustes</h3>
		                      <button onclick="loadTables()">Mesas</button>
		                      <button onclick="loadStaff()">Personal</button>
		                      <button  onclick="loadRestaurant()">Restaurante</button>
		                      <button>Otros</button>
                            </div>
                       <div class="col-sm-10">

	                       <div class="well" id="content">
                           </div>
                          </div>

                    </div>`;

}

function loadTables(){
     frame = document.getElementById('content');
     frame.innerHTML = `<h4> Mesas </h4>
                        <p>Mesa actual : ${currentTable} </p>

                        <div>
                            <label> Mesa </label> <button class='btn-success' onclick="addTable('M')">Añadir</button>
                            <label> Terraza </label> <button  class='btn-success' onclick="addTable('T')">Añadir</button>
                            <label> Barra </label> <button class='btn-success' onclick="addTable('B')">Añadir</button><br>
                            <button class='btn-danger' onclick="removeTable(${currentTable},${currentTableID})">Eliminar</button>
                        </div>

                        <div >
                            <ul id="tableList">Cargando...</ul>
	                    </div>`;
     get("tables", function(){
			"use strict";
			let list = document.getElementById('tableList');
			list.innerHTML = '';

			for (let table of this.response){
				list.insertAdjacentHTML('beforeend', `<li onclick="selectTable(${table.number},${table.id})">${table.type_table}${table.number}</li>`);
			}
	});
}

function selectTable(newTable,id){
    currentTable = newTable;
    currentTableID = id;
    loadTables();
}

function addTable(type){
   var valores = Object();
   valores.number=0;
   valores.type_table=type;
   valores.is_avaible = true;
   valores.restaurant = 3;

   post("tables/", function(){
		loadTables();
	}, valores, true);
}

function removeTable(num,id){
     if (confirm('¿Esta seguro de borrar la mesa '+num+'?')){
       _delete("tables/"+id+"/",function(){loadTables();},true);
    }
    return false;
}

function loadStaff(){
     frame = document.getElementById('content');
     frame.innerHTML = `<h4> Personal </h4>
                        <div id='staffPanel'>
                            <table class='table'>
                            <thead>
                            <th></th>
                            <th>Nombre</th>
                            <th>Cargo</th>
                            <th>Sueldo/hora</th>
                            <th>Activo</th>
                            <th>Notas</th>
                            <tbody id='staffList'>
                            </tbody>
                            </table>
	                    </div>`;
     get("staff/", function(){
			"use strict";
			let list = document.getElementById('staffList');
			list.innerHTML = '';

			for (let table of this.response){
				list.insertAdjacentHTML('beforeend', `<tr>
                                                        <td><button onclick='removeStaff(${table.id})' id='staffInput' class="glyphicon glyphicon-remove btn-danger"></button></td>
                                                        <td><input type='text' class="form-control" name='first_name' id='first_name${table.id}' value='${table.first_name}' readonly>
                                                        <input type='text' class="form-control" name='last_name' id='last_name${table.id}' value='${table.last_name}' readonly></td>
                                                        <td><p id='rol${table.id}'>${table.role_code}</p></td>
                                                        <td><input type='text'  class="form-control-addon"  id='hourly_rate${table.id}' name='hourly_rate' value=${table.hourly_rate} readonly>
                                                        <td><input type='checkbox' readonly name='is_active${table.id}'  id='is_active${table.id}'  class="form-control"></td>
                                                        <td><input type='text'  readonly  class="form-control-addon" id='notes${table.id}' name='notes' value='${table.notes}'></td>
                                                        <td id='editButton${table.id}'><button class="glyphicon glyphicon-pencil btn-warning" onclick='allowEditStaff(${table.id})'></button></td>
                                                       </tr>`);
                
                document.getElementById('is_active'+table.id).checked=table.is_active;
			}
          list.insertAdjacentHTML('beforeend',`<tr><td><button onclick='showStaffForm()' class="glyphicon glyphicon-plus btn-success" data-toggle="modal" data-target="#modalUser1"></button></td></tr></table>`);
	});
}

function allowEditStaff(id_user){
    var rol = document.getElementById('rol'+id_user);

    rol.innerHTML = '';
    rol.insertAdjacentHTML('beforeend',` <select id='role${id_user}'>
                                            <option value='M'>Manager</option>
                                            <option value='W'>Camarero</option>
                                            <option value='B'>Barman</option>
                                            <option value='K'>Cocinero</option>
                                </select>`);

    document.getElementById('first_name'+id_user).readOnly=false;
    document.getElementById('last_name'+id_user).readOnly=false;
    document.getElementById('is_active'+id_user).readOnly=false;
    document.getElementById('hourly_rate'+id_user).readOnly=false;
    document.getElementById('notes'+id_user).readOnly=false;

    var button = document.getElementById('editButton'+id_user);
    button.innerHTML='';
    button.insertAdjacentHTML('beforeend',`<button class="btn-warning"  onclick='editStaff(${id_user})'>Guardar</button>`);
}

function editStaff(id_user){
    var valores = Object();

    valores.first_name = document.getElementById('first_name'+id_user).value;
	valores.last_name = document.getElementById('last_name'+id_user).value;
    valores.role_code =  document.getElementById('role'+id_user).value;;
    valores.hourly_rate = document.getElementById('hourly_rate'+id_user).value;
    valores.is_active =  document.getElementById('is_active'+id_user).checked;
    valores.notes = document.getElementById('notes'+id_user).value;
    valores.restaurant = 2;

     put('staff/'+id_user+'/', function(){
		loadStaff();
	}, valores, true);
}

function removeStaff(id_user){
    if(confirm("Confirme el borrado")){
        _delete('staff/'+id_user+'/',function(){loadStaff();},true);
    }
}

function showStaffForm(){
    let list = document.getElementById('staffPanel');
    list.innerHTML='';
    list.insertAdjacentHTML('beforeend',`
                                        <div class="modal fade" id="modalUser1" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	                                       <div class="modal-dialog" role="document">
		                                      <div class="modal-content">
			                                     <div class="modal-header">
				                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
					                               <span aria-hidden="true">&times;</span></button>
				                                    <h4 class="modal-title" id="myModalLabel">Usuario para el empleado:   (Paso 1 de 2)</h4>
			                                     </div>
			                                 <div class="modal-body">
                                                <form onsubmit='return createUser(this);'>
				                                <label>Nombre Usuario</label> <input type='text' name="username"><br>
                                                <label>Contraseña</label><input type='password' name="pass"><br>
                                                <label>Repetir Contraseña</label><input type='password' name="passRepeated"><br>

                                            <div class="modal-footer">
                                            <p>Nota:Estos datos deben ser facilitados al empleado para poder conectarse y podrán ser modificados.</p>
                                            <button type='submit' class='btn-success'>Continuar</button>
                                            </form>
                                            </div>
			                             </div></div></div></div>

                                         <div class="modal fade" id="modalUser2" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	                                       <div class="modal-dialog" role="document">
		                                      <div class="modal-content">
			                                     <div class="modal-header">
				                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
					                               <span aria-hidden="true">&times;</span></button>
				                                    <h4 class="modal-title" id="myModalLabel">Datos del empleado:   (Paso 2 de 2)</h4>
			                                     </div>
			                                 <div class="modal-body">
                                                <form onsubmit='return addStaff(this)'>
                                                <input type='hidden' id='user' name='user'><br>
				                                <label>Nombre</label><input type='text' class=class="input-group" name='first_name' placeholder='Nombre'><br>
                                                <label>Apellidos</label><input type='text' name='last_name' placeholder='Apellidos'><br>
                                                <label> Cargo </label><select name='role'>
                                                    <option value='M'>Manager</option>
                                                    <option value='W'>Camarero</option>
                                                    <option value='B'>Barman</option>
                                                    <option value='K'>Cocinero</option>
                                                </select><br>
                                                <label>Sueldo/hora</label><input type='text' placeholder='' name='hourly_rate'><br>
                                                <label>Activo</label><input type='checkbox' name='is_active' checked><br>
                                                <label>Anotaciones</label><input type='text' name='notes' placeholder='Notas'><br>

                                            <div class="modal-footer">
                                                <p>Nota:Estos datos podrán ser modificados en el futuro.</p>
                                                  <button type='submit' class='btn-success'>Finalizar</button>
                                                </form>
                                            </div>
			                             </div></div></div></div>`);
}

function addStaff(form){
    var valores = Object();

	valores.first_name = form.first_name.value;
	valores.last_name = form.last_name.value;
    valores.role_code = form.role.value;
    valores.hourly_rate = form.hourly_rate.value;
    valores.is_active = form.is_active.checked;
    valores.restaurant = 2;
    valores.user = form.user.value;
    valores.notes = form.notes.value;

	post("staff/", function(){
				loadStaff();
			}, valores, true);
    	return false;
}

function loadRestaurant(){
    frame = document.getElementById('content');
    frame.innerHTML=`<div id='restInfo'></div>`;
    get("restaurants/",function(){
        "use strict";
        let list = document.getElementById('restInfo');
        list.innerHTML = '';

        for (let table of this.response){
				list.insertAdjacentHTML('beforeend',`
                                                    <div class='row'><div class='col-md-6'><input type='hidden' id='id' value='${table.id}'>
                                                            <label>Nombre</label><input type='text' class="form-group" id='name' value='${table.name}'><br>
                                                            <input type='hidden' id='owner' value='${table.owner}'><br>
                                                            <fielset>
                                                                <legend>Dirección</legend>
                                                                <label>Numero</label><input type='text' id='number' class='form-group'><br>
                                                                <label>Calle</label><input type='text' name='street' id='address' class="form-group" value='${table.address}'><br>
                                                                <label>Localidad</label><input type='text' id='city' class="form-group" name='city' value='${table.city}'><br>
                                                                <label>Provincia</label><input type='text' id='province' value='${table.province}'>
                                                            </fielset></div>
                                                        <div class='col-md-6'>
                                                            <div><label>Lat:</label><input id='lat' value='${table.lat}' readonly>
                                                                 <label>Long:</label><input id='long' value='${table.lng}' readonly>
                                                            </div>
                                                            <div id='map' style="height:300px"></div>
                                                        </div>
                                                    </div>
                                                        <div class='row' id='editRest'>
                                                            <button class='btn pull-right' onclick='editRestaurant(${table.id})'>Editar</button>
                                                        </div>`);
            initMap(table.lat,table.lng);
			}

    });
}

function initMap(lat,long){
    var my_rest = {lat: lat, lng: long};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 14,
          center: my_rest
        });
        var marker = new google.maps.Marker({
          position: my_rest,
          map: map
        });

}

function getLatLong(){
    var n = document.getElementById('number').value;
    var street = document.getElementById('address').value.split(",");
    var city = document.getElementById('city').value;
    var prov = document.getElementById('province').value;

    get(n+"+"+street+"+"+city+"+"+prov,function(){var coords = this.response.results[0].geometry.location;
                                                                     var lat = coords.lat;
                                                                     var lng = coords.lng;
                                                                     document.getElementById('lat').value = lat;
                                                                     document.getElementById('long').value = lng;
                                                                     initMap(lat,lng);},
        true,"https://maps.googleapis.com/maps/api/geocode/json?address=",false);
}

function editRestaurant(id_rest){
    getLatLong();
    var n = document.getElementById('number').value;
    var address = document.getElementById('address').value;

    var valores = Object();
    valores.name = document.getElementById('name').value;
    valores.address = address;
    valores.lat =  parseFloat(document.getElementById('lat').value);
    valores.lng = parseFloat(document.getElementById('long').value);
    valores.city = document.getElementById('city').value;
    valores.province = document.getElementById('province').value;
    valores.owner = document.getElementById('owner').value;

    put('restaurants/'+id_rest+'/', function(){initMap(valores.lat,valores.lng);}, valores);
}

function seeTables(){
	main.innerHTML = `<h3>Mesas</h3>
		<ul id="tablesList">Cargando...</ul>`;
	
	get("tables/", function(){
		"use strict";
		let list = document.getElementById('tablesList');
		list.innerHTML = '';

		for (let table of this.response){
			list.insertAdjacentHTML('beforeend', `<li onclick="getTicket(${table.id}, '${table.type_table}${table.number}')">${table.type_table}${table.number}</li>`);
		}
	});
}

function getTicket(tableID, tableName){
	currentTableID = tableID;
	currentTable = tableName;
	loadTPV();
}

function loadFamily(name){
	familyWanted = name;
	document.getElementById('productsList').innerHTML = "Cargando...";

	get("products/?family=" + encodeURIComponent(name), function(){
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

function showTicket(ticket){
	console.log(ticket);
	
	document.getElementById('totalCost').innerText = "Total cuenta: " + ticket.cost + "€";
	document.getElementById('ticketID').innerText = "Número de ticket: " + ticket.pk;
	
	var list = document.getElementById('ticketList');
	list.innerHTML = '';
	
	// for...
}

function createTicket(){
	newTicket = Object();
	newTicket.staff = sessionStorage['userID'];
	newTicket.restaurant = sessionStorage['restaurantID'];
	newTicket.table = currentTableID;
	
	post("tickets/", function(){
		showTicket(this.response);
	}, newTicket);
}

function loadTPV(){
	main.innerHTML = `<div class="container-fluid">
		<div class="row content">
		 <div class="col-sm-1 sidenav " style="width: 12%">
		     <div class="btn-group-vertical" style="width: 110%">
		     <button onclick="seeTables()" type="button" class="btn btn-primary">Ver Mesas</button>
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
		         <p id="totalCost">Total cuenta</p>
		         <p>Camarero: ${sessionStorage['username']}</p>
		         <p id="tableName">Número de Mesa</p>
		         <p id="ticketID">Número de Ticket</p>
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
		         <ul id="ticketList">Contiene una lista dinámica con todos los productos del ticket actual</ul>
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
				list.insertAdjacentHTML('beforeend', `<li onclick="loadFamily('${family.name}')">${family.name}</li>`);
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
	
	if (currentTable){
		document.getElementById('ticketList').innerText = "Cargando...";
		document.getElementById('tableName').innerText = "Mesa: " + currentTable;
	
		get("tickets/?is_closed=false&table=" + currentTableID, function(){
			if (this.response.length == 0) createTicket();
			else{ showTicket(this.response[0]); }
		});	
	}
}

function loadApp(){
	document.body.innerHTML = `<header>
	<nav class="navbar navbar-inverse">
	<div class="container">
		<div class="navbar-header">
		  <a class="navbar-brand" href="#">Mappeat</a>
		</div>
			<div class="navbar-collapse collapse navbar-right ">
				<button onclick="loadStore()">Almacén</button>
				<button onclick="loadMenu()">Menú</button>
				<button onclick="loadTPV()">TPV</button>
				<button>Informes</button>
				<button onclick="loadSettings()">Ajustes</button>
				<button onclick="location.reload()">Salir</button>
			</div>
	</div>
	</nav>
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

function createUser(form){
	if( form.pass.value != form.passRepeated.value ){
		alert("Error: Las contraseñas deben coincidir.");
		return false;
	}

	var valores = Object();
	valores.username = form.username.value;
	valores.password = form.pass.value;

	post("users/", function(){
		$('#modalUser1').modal('hide');
		$('#modalUser2').modal('show');
		get("users/?username=" + form.username.value, function(){ document.getElementById('user').value = this.response[0].pk; });
	}, valores);

	return false;
}

function login(form){
	var valores = Object();
	valores.username = form.username.value;
	valores.password = form.pass.value;
	
	sessionStorage['username'] = valores.username;	
	let pendingData = 2;

	post("login/", function(){
		get("restaurants/", function(){
			sessionStorage['restaurantID'] = this.response[0].id;
			pendingData -= 1;
			if (pendingData == 0) loadApp();
		});
		
		get("users/?username=" + valores.username, function(){
		get("staff/?user=" + this.response[0].pk, function(){
			sessionStorage['userID'] = this.response[0].id;
			pendingData -= 1;
			if (pendingData == 0) loadApp();
		});
		});
	}, valores, true, "/rest-auth/");

	return false;
}

function loadStore(){
    main.innerHTML = `<div class="container-fluid">
                        <div class="col-sm-10">
		                      <div class="well" id="content">
                                  <h4> Almacen </h4>
                                  <div id='panel'>
                                    <table class='table'>
                                    <thead>
                                    <th></th>
                                    <th>Producto</th>
                                    <th>Formato</th>
                                    <th>Código de barras</th>
                                    <th>Unidades</th>

                                    <tbody id='storeList'></tbody>
                                    </table>
	                               </div>
                              </div>
                        </div>
                     </div>`;

    let list = document.getElementById('storeList');
    get('inventory/',function(){
                        'user strict';

                        list.innerHTML='';

                        for(let table of this.response){
                            get('suplies/'+table.supply,function(){
                                list.insertAdjacentHTML('beforeend',`<tr><td><button onclick='removeInventory(${table.id})' class="glyphicon glyphicon-remove btn-danger"></button></td><td>${this.response.name}</td><td>${this.response.mesure_unity}</td><td>${this.response.barcode}</td><td>${table.quantity}</td></tr>`);}
                               );
                        }
                         list.insertAdjacentHTML('afterend',`<tr><td><button onclick='newSupplyForm()' class="glyphicon glyphicon-plus btn-success" data-toggle="modal" data-target="#modalStore"></button></td></tr></table>`);
    });
}

function newSupplyForm(){
    $('#modalIngredient').modal('hide');
    let list = document.getElementById('panel');
    list.insertAdjacentHTML('beforeend',`
                                        <div class="modal fade" id="modalStore" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
	                                       <div class="modal-dialog" role="document">
		                                      <div class="modal-content">
			                                     <div class="modal-header">
				                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
					                               <span aria-hidden="true">&times;</span></button>
				                                    <h4 class="modal-title" id="myModalLabel">Registrar Nuevo Artículo</h4>
			                                     </div>
			                                 <div class="modal-body">
                                                <form id='newSupply' onsubmit='return addSupply(this);'>
				                                <label>Nombre</label><input type='text'  name='name'><br>
                                                <label>Formato</label><select name='mesure_unity' id='format'></select><br>
                                                <label>Código de Barras</label><input type='text' name='barcode'><br>
                                                <label>Almacenable</label><input type='checkbox' name='storable' checked><br>
                                                <label>Cantidad</label><input type='number' name='quantity'>
                                            <div class="modal-footer">
                                            <button type='submit' class='btn-success'>Continuar</button>
                                            </form>
                                            </div>


			                             </div></div></div></div>`);
  fillFormats();
}

function fillFormats(){

    get('mesureUnities/',function(){
        let list = document.getElementById('format');
        list.innerHTML='';
        for(let format of this.response){
            list.insertAdjacentHTML('beforeend',`<option value='${format.id}'>${format.name}</option>`);
        }
    });
}

function addSupply(form){
    var valoresSupply = new Object();
    var valoresInventory = new Object();

    valoresSupply.name = form.name.value;
    valoresSupply.is_storable = form.storable.checked;
    valoresSupply.barcode = form.barcode.value;
    valoresSupply.mesure_unity = form.mesure_unity.value;
    valoresSupply.category = 2; // La categoria 2 se corresponde a 'Articulo'
    
    valoresInventory.quantity = form.quantity.value;
    valoresInventory.restaurant = 2;
    valoresInventory.available = true;

    post("suplies/", function(){
		valoresInventory.supply = this.response['id'];
        // is_storable indica si queremos almacenarlo en Inventory
        if (valoresSupply.is_storable){
            post('inventory/',function(){ loadStore(); },valoresInventory,true);
        }
        $('#modalStore').modal('hide');
	}, valoresSupply, true);

    

	return false;
}

function removeInventory(id){
     if (confirm('Confirme el borrado')){
       _delete("inventory/"+id+"/",function(){loadStore();},true);
    }
    return false;
}

function loadMenu(){
      main.innerHTML = `<div class="container-fluid">
                        <div class="col-sm-10">
		                      <div class="well" id="content">
                                  <h2> Menu </h2>
                                    <div id='panel'>
                                    <table class='table'>
                                    <thead></thead>
                                    <tbody id='menuList'></tbody>
                                    </table>
	                               </div>
                              </div>
                        </div>
                     </div>`;
     get('products/',function(){
         'use strict';
         let list = document.getElementById('menuList');
         list.innerHTML = '';
         
         for (let product of this.response ){
             get ('iva/'+product.iva_tax,function(){
                        list.insertAdjacentHTML('beforeend',`<tr><td class="active"><h4>${product.name}</h4></td><td> <a onclick='editProductForm(${product.id})' data-toggle="modal" data-target="#modalEditProduct" >Editar</a></td><td><button onclick="removeProduct(${product.id})" class="glyphicon glyphicon-remove btn-danger"></button></td></tr><tr><td><img class="img-rounded" src='' alt='icono${product.icon}'></td><td><div class='well' id='ingredients${product.id}'></div></td><td><p class="bg-primary text-white">${product.price_with_tax}€</p><p class='bg-danger'>${this.response.strTax}</p><p class='bg-success'>${product.price_as_complement_with_tax}€</p></td>
                        <td><div class='well'>STATS</div></td>
                                                      </tr>`);
                
                            getIngredients(product.id);  
    });
             
           }
         list.insertAdjacentHTML('afterend',`<tr><td><button onclick='showProductForm()' class="glyphicon glyphicon-plus btn-success" data-toggle="modal" data-target="#modalMenu"></button></td></tr></table>`);           
    });
}

function getIngredients(product){
    let frame = document.getElementById('ingredients'+product);
    frame.innerHTML = '';
    get('ingredients/?product='+product,function(){
        frame.insertAdjacentHTML('beforeend',`<ul class="list-group">`);
        for (let ingredient of this.response){
            get('suplies/'+ingredient.supply, function(){  frame.insertAdjacentHTML('beforeend',`<li class="list-group-item"><span class='glyphicon glyphicon-minus' onclick='removeIngredient(${ingredient.id})'></span>   ${this.response.name}</li>`);});
        }
        frame.insertAdjacentHTML('afterend',`</ul><span onclick='newIngredient(${product})' data-toggle="modal" data-target="#modalIngredient" class="glyphicon glyphicon-plus  pull-right"></span>`);

    });
}

function showProductForm(){
    let list = document.getElementById('panel');
    list.insertAdjacentHTML('beforeend',`
                                        <div class="modal fade" id="modalMenu" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
	                                       <div class="modal-dialog" role="document">
		                                      <div class="modal-content">
			                                     <div class="modal-header">
				                                   <button type="button" class="close" data-dismiss="modal" aria-label="Close">
					                               <span aria-hidden="true">&times;</span></button>
				                                    <h4 class="modal-title" id="myModalLabel">Registrar Nuevo Producto</h4>
			                                     </div>
			                                 <div class="modal-body">
                                                <form onsubmit='return addProduct(this);'>
				                                    <label>Nombre</label><input type='text' class='form-group' name='name'><br>
                                                    <label>Precio con IVA</label><input type='number' min='0.0' step="0.01"  class='form-group' name='price_with_tax'><br>
                                                    <label>Precio con complemento</label><input type='number'  class='form-group' min='0.0' step="0.01" name='price'><br>
                                                    <label>IVA</label><select  class='form-group' name='tax' id='iva_select'></select><br>
                                                    <label>Principal</label><input type='checkbox'  class='form-group' name='principal'><br>
                                                    <label>Complemento</label><input type='checkbox'  class='form-group' name='can_be_complement'><br>
                                                    <label>Producto</label><select class='form-group' name='product' id='product_select'></select><br>
                                            <div class="modal-footer">
                                            <button type='submit' class='btn-success'>Continuar</button>
                                            </form>
                                            </div>
			                             </div></div></div></div>`);
    
    get('iva/',function(){
        let list = document.getElementById('iva_select');
        list.innerHTML = '';
        for(let item of this.response){
            list.insertAdjacentHTML('beforeend',`<option value=${item.id}>${item.name}</option>`);
        }
    });
    
    get('product_classes/',function(){
        let list = document.getElementById('product_select');
        list.innerHTML = '';
         for(let item of this.response){
            list.insertAdjacentHTML('beforeend',`<option value=${item.id}>${item.name}</option>`);
        }
    });
}

function addProduct(form){
    var valores = new Object();
    valores.restaurant = 2 ;
    valores.name = form.name.value;
    valores.price_with_tax = form.price_with_tax.value;
    valores.price_as_complement_with_tax = form.price.value;
    valores.iva_tax = form.tax.value;
    valores.principal = form.principal.checked;
    valores.can_be_complement = form.can_be_complement.checked;
    valores.product = form.product.value;
    
    post('products/',function(){$('#modalMenu').modal('hide');
                                loadMenu();},
                            valores,true);
    
    return false;
}

function removeProduct(product){
    if (confirm('¿Desea borrar el producto?')){
       _delete("products/"+product+"/",function(){loadMenu();},true);
    }
    return false;
}

function newIngredient(product){
    let frame = document.getElementById('panel');
    frame.insertAdjacentHTML('beforeend',`
                                        <div class="modal fade" id="modalIngredient" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
	                                       <div class="modal-dialog" role="document">
		                                      <div class="modal-content">
			                                     <div class="modal-header">
				                                   <button type="button" class="close" data-dismiss="modal" aria-label="Close">
					                               <span aria-hidden="true">&times;</span></button>
				                                    <h4 class="modal-title" id="myModalLabel">Añadir Ingrediente</h4>
			                                     </div>
			                                 <div class="modal-body">
                                                <form onsubmit='return addIngredient(this)'>
                                                    <label>Cantidad</label><input type='number' min='0.0' class='form-group' name='quantity'><br>
                                                    <label>Suministro</label><select  class='form-group' name='supply' id='supply_select'></select>
                                                    <span class='btn btn-primary pull-right' onclick='newSupplyForm()' data-toggle="modal" data-target="#modalStore">Nuevo Suministro</span>
                                                    <input type='hidden' value=${product} name='product'>
                                                   
                                            <div class="modal-footer">
                                            <button type='submit' class='btn-success'>Continuar</button>
                                            </form>
                                            </div>
			                             </div></div></div></div>`);
    
    get('suplies/',function(){
        let list = document.getElementById('supply_select');
        list.innerHTML = '';
        for(let item of this.response){
            list.insertAdjacentHTML('beforeend',`<option value=${item.id}>${item.name}</option>`);
        }
    });
    
}

function addIngredient(form){
    var valores = new Object();
    valores.product = form.product.value;
    valores.supply = form.supply.value;
    valores.quantity = form.quantity.value;
    
    post('ingredients/',function(){$('#modalIngredient').modal('hide');
                                    loadMenu();}
                                    ,valores,true);
    return false;
}

function removeIngredient(id){
   if (confirm('Confirme el borrado')){
       _delete("ingredients/"+id+"/",function(){loadMenu();},true);
    }
    return false;
} 

function editProductForm(product){
    get('products/'+product,function(){
        let list = document.getElementById('panel');
    list.insertAdjacentHTML('beforeend',`
                                        <div class="modal fade" id="modalEditProduct" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
	                                       <div class="modal-dialog" role="document">
		                                      <div class="modal-content">
			                                     <div class="modal-header">
				                                   <button type="button" class="close" data-dismiss="modal" aria-label="Close">
					                               <span aria-hidden="true">&times;</span></button>
				                                    <h4 class="modal-title" id="myModalLabel">Editar Producto</h4>
			                                     </div>
			                                 <div class="modal-body">
                                                <form onsubmit='return editProduct(this);'>
                                                    <input type='hidden' name='id' value='${product}'>
                                                    <input type='hidden' name='restaurant' value='${this.response.restaurant}'>
				                                    <label>Nombre</label><input type='text' class='form-group' value='${this.response.name}' name='name'><br>
                                                    <label>Precio con IVA</label><input type='number' min='0.0' step="0.01"  class='form-group' name='price_with_tax' value='${this.response.price_with_tax}' ><br>
                                                    <label>Precio con complemento</label><input type='number'  class='form-group' min='0.0' step="0.01" name='price' value='${this.response.price_as_complement_with_tax}'><br>
                                                    <label>IVA</label><select  class='form-group' name='tax' id='iva_select'></select><br>
                                                    <label>Principal</label><input type='checkbox'  class='form-group' id='principal' name='principal'><br>
                                                    <label>Complemento</label><input type='checkbox'  class='form-group' id='complement' name='can_be_complement'><br>
                                                    <label>Producto</label><select class='form-group' name='product' id='product_select'></select><br>
                                            <div class="modal-footer">
                                            <button type='submit' class='btn-success'>Continuar</button>
                                            </form>
                                            </div>
			                             </div></div></div></div>`);
       document.getElementById('principal').checked = this.response.principal;
       document.getElementById('complement').checked = this.response.can_be_completent;
    
    get('iva/',function(){
        let list = document.getElementById('iva_select');
        list.innerHTML = '';
        for(let item of this.response){
            list.insertAdjacentHTML('beforeend',`<option value=${item.id}>${item.name}</option>`);
        }
    });
    
    get('product_classes/',function(){
        let list = document.getElementById('product_select');
        list.innerHTML = '';
         for(let item of this.response){
            list.insertAdjacentHTML('beforeend',`<option value=${item.id}>${item.name}</option>`);
        }
    });
    })
    
}

function editProduct(form){
    var valores = new Object();
    
    valores.restaurant = form.restaurant.value;
    valores.name = form.name.value;
    valores.price_with_tax = form.price_with_tax.value;
    valores.price_as_complement_with_tax = form.price.value;
    valores.iva_tax = form.tax.value;
    valores.principal = form.principal.checked;
    valores.can_be_complement = form.can_be_complement.checked;
    valores.product = form.product.value;
    
      put('products/'+form.id.value+'/', function(){
        $('#modalEditProduct').modal('hide');
		loadMenu();
	}, valores, true);
    
    return false;
}
