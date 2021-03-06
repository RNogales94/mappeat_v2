var main;
var familyWanted;
var currentTable;
var currentTableID;
var currentTicketID;
var combined;
var currentTicketDetailID;

function loadSettings(){
	main.innerHTML = `<div class=" content container-fluid">
                        <div class='row'>
                       	<div class="col-md-2 sidebar">
                            <div class="list-group text-center">
                            <span><h3>Ajustes</h3></span>
                               <a class="list-group-item" onclick='loadTables()'> Mesas</a>
                               <a class="list-group-item" onclick='loadStaff()'> Personal</a>
                               <a class="list-group-item" onclick='loadRestaurant()'> Restaurante</a>
                               <a class="list-group-item" onclick='void(0)'>Otros</a>
                            </div>
                        </div>
                       <div class="col-sm-10">
	                       <div class="well" id="content">
                           </div>
                        </div>
                        </div>
                      </div>`;

}

function loadTables(){
     frame = document.getElementById('content');
     frame.innerHTML = `<h4> Mesas </h4>

                            <div id='tablesPanel'>
                            <table class='table'>
                            <thead>
                            <th>MESAS   <span class='glyphicon glyphicon-plus text-success' onclick='addTable("M")'></span></th>
                            <th>BARRA   <span class='glyphicon glyphicon-plus text-success' onclick='addTable("B")'></span></th>
                            <th>TERRAZA  <span class='glyphicon glyphicon-plus text-success' onclick='addTable("T")'></span></th>
                            <tbody>
                                <tr>
                                    <td><div class='col-md-4' id='tables'></div></td>
                                    <td><div class='col-md-4' id='bar'></div></td>
                                    <td><div class='col-md-4' id='terrace'></div></td>
                                </tr>
                            </tbody>
                            </table>`;


     get("tables", function(){
			"use strict";
			let tables = document.getElementById('tables');
            let terrace = document.getElementById('terrace');
            let bar = document.getElementById('bar');

			tables.innerHTML = '';
            terrace.innerHTML = '';
            bar.innerHTML = '';

			for (let table of this.response){
                switch(table.type_table) {
                    case "B":
                        bar.insertAdjacentHTML('beforeend',`<span class='glyphicon glyphicon-minus text-danger' onclick='removeTable(${table.id})'></span> ${table.type_table}${table.number}<br>`)
                        break;
                    case "M":
                        tables.insertAdjacentHTML('beforeend',`<span class='glyphicon glyphicon-minus text-danger' onclick='removeTable(${table.id})'></span>${table.type_table}${table.number}<br>`)
                        break;
                    case "T":
                        terrace.insertAdjacentHTML('beforeend',`<span class='glyphicon glyphicon-minus text-danger' onclick='removeTable(${table.id})'></span>${table.type_table}${table.number}<br>`)
                        break;

                }
            }
	});
}


function addTable(type){
   var valores = Object();
   valores.number=0;
   valores.type_table=type;
   valores.is_avaible = true;
   valores.restaurant = sessionStorage['restaurantID'];

   post("tables/", function(){
		loadTables();
	}, valores, true);
}

function removeTable(id){
     if (confirm('¿Esta seguro de borrar la mesa ?')){
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
    valores.restaurant = sessionStorage['restaurantID'];

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
    valores.restaurant = sessionStorage['restaurantID'];
    valores.user = form.user.value;
    valores.notes = form.notes.value;

	post("staff/", function(){
                $('#modalUser2').modal('hide');
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
                                                            <label>NIF</label><input type='text' class='form-group' id='nif_input' value='${table.nif}'><br>
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
                                                            <div id='map'></div>
                                                        </div>
                                                    </div>
                                                        <div class='row' id='editRest'>
                                                            <button class='btn btn-warning pull-right' onclick='editRestaurant(${table.id})'>Editar</button>
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
    valores.nif = document.getElementById('nif_input').value;
    
    put('restaurants/'+id_rest+'/', function(){initMap(valores.lat,valores.lng);}, valores);
}

function seeTables(){
	main.innerHTML = `  <div class='row content'>
                        <div class="btn-toolbar" role="toolbar">
                            <button type="button" class="btn btn-default btn-lg"  onclick='loadTPV()'>
                            <span class='glyphicon glyphicon-arrow-left'></span>
                            </button>
                            <h3 class="text-center">Mesas</h3>
                        </div>
                      <div class = 'well'>
                          <svg id='tableMap'></svg>
                      </div></div>`;

	get("tables/", function(){
		"use strict";
			let map = document.getElementById('tableMap');
			let n = this.response.length;
			map.innerHTML = '';

			if (n<=0){
				map.insertAdjacentHTML('beforebegin', `<p>Antes de poder ver mesas tienes que crearlas en Ajustes -> Mesas.</p>
				<button onclick="loadSettings(); loadTables()">Ir directamente a ajustes de mesas (Ajustes -> Mesas)</button>`);
			}

        //numero de columnas
        let cols = 5;
        //tamaño del cuadrado
        let size = 100;
        let rows = Math.floor(n/cols)+1;

        //ajusta altura
        map.setAttribute('height',rows*1.2*size);

        let table;
        let available;

        for (var i = 0;  i < rows ; i += 1){
            for (var j = 0 ; j < cols ; j += 1){
                if( i*cols+j < n){
                     table =  this.response[i*cols+j];
                     available = "#00FF00";
                        if(!table.is_available)
                            available = "#FF0000";
                     map.insertAdjacentHTML('beforeend',`<rect x=${map.width.baseVal.value*j/cols+1} y=${map.height.baseVal.value*i/rows} width=${size} height=${size} style="fill:${available}" onclick="getTicket(${table.id}, '${table.type_table}${table.number}')"></rect>
            <text x=${map.width.baseVal.value*j/cols+40} y=${map.height.baseVal.value*i/rows+50} font-family="Verdana"
        font-size="20" onclick="getTicket(${table.id}, '${table.type_table}${table.number}')">${table.type_table}${table.number}</text>`);
                }
                else break;
            }
        }


	});
}

function getTicket(tableID, tableName){
	currentTableID = tableID;
	currentTable = tableName;

    //marca la mesa como ocupada
    get('tables/'+currentTableID+'/',function(){
         var valores = this.response;
         valores.is_available = false;
         put('tables/'+currentTableID+'/',function(){
                                                loadTPV();},valores,true)});
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
					list.insertAdjacentHTML('beforeend', `<li onclick="addTicketDetail(${product.id})">${product.name}</li>`);
				}
			}
	});
}

var totalCost;
var totalRest;
var ticketTable;
var partialTable;
var partialCost;
var partialRest;
var divisions;
var input;
var customTotal;
var customRest;
var activeInput;

function divide(node, divisor){
	return (node.innerText / divisor).toFixed(2);
}

function calculateSplit(){
	totalRest.innerText = (input.value - totalCost.innerText).toFixed(2);
	partialRest.innerText = (input.value - partialCost.innerText).toFixed(2);
	customRest.innerText = (input.value - customTotal.value).toFixed(2);
	divisions.innerText = `${divide(totalCost, 2)} (2), ${divide(totalCost, 3)} (3), ${divide(totalCost, 4)} (4), ${divide(totalCost, 5)} (5), ${divide(totalCost, 6)} (6)`;
}

function addAmount(amount){
	activeInput.value = (parseFloat(activeInput.value) + amount).toFixed(2);
	calculateSplit();
}

function removeFromPartial(line){
	let name = line.querySelector("[name=name]").innerText;
	let quantity = line.querySelector("[name=quantity]").innerText;
	let price = line.querySelector("[name=price]").innerText;

	ticketTable.insertAdjacentHTML('beforeend', `<tr onclick="addToPartial(this)">
		<td name="name">${name}</td>
		<td name="quantity">${quantity}</td>
		<td><span name="price">${price}</span>€</td>
	</tr>`);

	totalCost.innerText = ( parseFloat(totalCost.innerText) + parseFloat(price) ).toFixed(2);
	partialCost.innerText = (partialCost.innerText - price).toFixed(2);
	calculateSplit();
	line.parentNode.removeChild(line);
}

function addToPartial(line){
	let lineName = line.querySelector("[name=name]").innerText;
	let lineQuantity = line.querySelector("[name=quantity]");
	let linePrice = line.querySelector("[name=price]");
	let unitPrice = linePrice.innerText / lineQuantity.innerText;

	if (parseInt(lineQuantity.innerText) == 1)
		line.parentNode.removeChild(line);
	else {
		lineQuantity.innerText = parseInt(lineQuantity.innerText) - 1;
		linePrice.innerText = (linePrice.innerText - unitPrice).toFixed(2);
	}

	totalCost.innerText = (totalCost.innerText - unitPrice).toFixed(2);
	partialCost.innerText = (parseFloat(partialCost.innerText) + parseFloat(unitPrice)).toFixed(2);
	calculateSplit();

	if (partialTable.lastChild && 'querySelector' in partialTable.lastChild && partialTable.lastChild.querySelector("[name=name]").innerText == lineName){
		let quantity = partialTable.lastChild.querySelector("[name=quantity]");
		let price = partialTable.lastChild.querySelector("[name=price]");
		quantity.innerText = parseInt(quantity.innerText) + 1;
		price.innerText = ( parseFloat(price.innerText) + parseFloat(unitPrice) ).toFixed(2);
	}
	else{
		partialTable.insertAdjacentHTML('beforeend', `<tr onclick="removeFromPartial(this)">
			<td name="name">${lineName}</td>
			<td name="quantity">1</td>
			<td><span name="price">${unitPrice.toFixed(2)}</span>€</td>
		</tr>`);
	}
}

function splitTicket(){
	main.innerHTML = `<div class='row content'>
            <div class="btn-toolbar" role="toolbar">
            <button type="button" class="btn btn-default btn-lg"  onclick='loadTPV()'>
                <span class='glyphicon glyphicon-arrow-left'></span>
            </button>
            <h3 class="text-center" >Dividir Ticket</h3></div>
          <div class='well row'>
		  <div class='well col-sm-4'>
          <h4>Cuenta restante</h4>
		  <table class='table'>
			<thead>
				<tr>
					<th>Producto</th>
					<th>Cantidad</th>
					<th>Precio</th>
				</tr>
			</thead>
			<tbody id="ticketTable">
			</tbody>
		</table>
		<p>Total: <span id="totalCost">0</span>€</p>
		<p>Resto: <span id="totalRest">0</span>€</p>
		<p>Divisiones: <span id="divisions"></span></p>
	</div>

	<div class='well col-sm-4'>
		<h4>Cuenta parcial</h4>
		<table class='table'>
			<thead>
				<tr>
					<th>Producto</th>
					<th>Cantidad</th>
					<th>Precio</th>
				</tr>
			</thead>
			<tbody id="partialTable">
			</tbody>
		</table>
		<p>Subtotal: <span id="partialCost">0</span>€</p>
		<p>Resto: <span id="partialRest">0</span>€</p>
		<button onclick="partialCost.innerText = 0; calculateSplit(); partialTable.innerHTML = ''">Limpiar</button>
	</div>
	<div class='well  col-sm-4'>
		<label>Lo que te ha dado el tío:</label>
		<input onfocus="activeInput = this" onclick="this.value = 0; calculateSplit()" oninput="calculateSplit()" value="0" id="input" type="number">
		<label>Lo que le quieres cobrar:</label>
		<input onfocus="activeInput = this" onclick="this.value = 0; calculateSplit()" oninput="calculateSplit()" value="0" id="customTotal" type="number">
		<ul clas="ul-tpv">
			<ul clas="ul-tpv">
				<li class='moneda euro2' onclick="addAmount(2)">2€</li>
				<li class='moneda euro1' onclick="addAmount(1)">1€</li>
			</ul>
			<ul clas="ul-tpv">
				<li class='moneda oro' onclick="addAmount(0.5)">50</li>
				<li class='moneda oro' onclick="addAmount(0.2)">20</li>
				<li class='moneda oro' onclick="addAmount(0.1)">10</li>
			</ul>
			<ul clas="ul-tpv">
				<li class='moneda cobre' onclick="addAmount(0.05)">5</li>
				<li class='moneda cobre' onclick="addAmount(0.02)">2</li>
				<li class='moneda cobre' onclick="addAmount(0.01)">1</li>
			</ul>
			<li class='billete euro5' onclick="addAmount(5)">5€</li>
			<li class='billete euro10' onclick="addAmount(10)">10€</li>
			<li class='billete euro20' onclick="addAmount(20)">20€</li>
			<li class='billete euro50' onclick="addAmount(50)">50€</li>
			<li class='billete euro100' onclick="addAmount(100)">100€</li>
		</ul>
		<p>Resto: <span id="customRest">0</span>€</p>
	</div>

<div class='row text-center'>
    <button class='btn btn-success btn-lg' onclick='charge()'>Cobrar</button>
</div>
    </div></div>`;

	totalCost = document.getElementById("totalCost");
	totalRest = document.getElementById("totalRest");
	ticketTable = document.getElementById("ticketTable");
	partialTable = document.getElementById("partialTable");
	partialCost = document.getElementById("partialCost");
	partialRest = document.getElementById("partialRest");
	divisions = document.getElementById("divisions");
	input = document.getElementById("input");
	customTotal = document.getElementById("customTotal");
	customRest = document.getElementById("customRest");
	activeInput = input;

	get("tickets/?is_closed=False&table=" + currentTableID, function(){
		var totalCost = document.getElementById('totalCost');
		totalCost.innerText = this.response[0].cost.toFixed(2);
		calculateSplit();

		var table = document.getElementById('ticketTable');

		for (let line of this.response[0].details){
			ticketTable.insertAdjacentHTML('beforeend', `<tr onclick="addToPartial(this)">
				<td name="name">${line.product_name}</td>
				<td name="quantity">${line.quantity}</td>
				<td><span name="price">${line.price.toFixed(2)}</span>€</td>
			</tr>`);
		}
	});
}

function showTicket(ticket){
	  document.getElementById('ticketID').innerText = "Número de ticket: " + ticket.pk;
	  document.getElementById('cashButton').innerText = ticket.cost.toFixed(2) + "€";
    document.getElementById('ticketTime').innerText = ticket.time + "  " + ticket.date;

	  var table = document.getElementById('ticketTable');
    var pending = document.getElementById('kitchenTicket');

    table.innerHTML = `<thead>
		<tr>
			<th></th>
			<th>Producto</th>
			<th>Cantidad</th>
			<th>Precio</th>
		</tr>
	</thead>
	<tbody>
	</tbody>`;
	table = table.lastChild;
	pending.innerHTML = '';

    for (let line of ticket.details){
		table.insertAdjacentHTML('beforeend', `<tr>
			<td><span class='glyphicon glyphicon-remove remove_button' onclick='removeTicketDetail(${line.pk})'></span> </td>
			<td>${line.product_name}</td>
			<td>${line.quantity}</td>
			<td onclick='showCalculator(${line.pk})'>${line.price.toFixed(2)}€</td>
		</tr>`);
        if (!line.sent_kitchen){
            pending.insertAdjacentHTML('beforeend', `<tr onclick="void(0)">
            <td>${line.product_name}</td>
			<td>${line.quantity}</td>
		</tr>`);
        }
	}
    table.insertAdjacentHTML('beforeend',`<tr><td></td><td><strong>Total:</strong><td></td><td><strong>${ticket.cost.toFixed(2)}€</strong></td></tr>`);
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

function loadTicket(){
	if (currentTable){
		document.getElementById('ticketTable').innerText = "Cargando...";
		document.getElementById('tableName').innerText = "Mesa: " + currentTable;

		get("tickets/?is_closed=False&table=" + currentTableID, function(){
			if (this.response.length == 0) createTicket();
			else{ 
                 currentTicketID = this.response[0].pk;
                 showTicket(this.response[0]); 
                }
		});
	}
}

function cancelTicket(){
    if(currentTableID){
	   if(confirm("¿Estás seguro de que deseas cancelar esta cuenta?")){
           get("tickets/?is_closed=False&table=" + currentTableID,function(){
                setTableFree();
                _delete('tickets/'+this.response[0].pk+'/',function(){});
                loadTPV();
            });

        }
    }
}

//mapa de mesas con onclick = cambio de mesa
function viewTables(){
    if(currentTableID){
    	main.innerHTML = `<div class='row content'>
                            <div class="btn-toolbar" role="toolbar">
                            <button type="button" class="btn btn-default btn-lg"  onclick='loadTPV()'>
                            <span class='glyphicon glyphicon-arrow-left'></span>
                            </button>
                            <h3 class="text-center">Mesas</h3>
                        </div>
                      <div class = 'well'>
                          <svg id='tableMap'></svg>
                      </div>
                      </div>`;

	get("tables/", function(){
		"use strict";
        let map = document.getElementById('tableMap');


        let n = this.response.length;
        //numero de columnas
        let cols = 5;
        //tamaño del cuadrado
        let size = 100;
        let rows = Math.floor(n/cols)+1;

        //ajusta altura
        map.setAttribute('height',rows*1.2*size);

        let table;
        let available;

        map.innerHTML = '';


        for (var i = 0;  i < rows ; i += 1){
            for (var j = 0 ; j < cols ; j += 1){
                if( i*cols+j < n){
                     table =  this.response[i*cols+j];

                        if(table.is_available){
                            available = "#00FF00";
                             map.insertAdjacentHTML('beforeend',`<rect x=${map.width.baseVal.value*j/cols+1} y=${map.height.baseVal.value*i/rows} width=${size} height=${size} style="fill:${available}" onclick="transferTable(${table.id},'${table.type_table}${table.number}')"></rect>
            <text x=${map.width.baseVal.value*j/cols+40} y=${map.height.baseVal.value*i/rows+50} font-family="Verdana"
        font-size="20" onclick="transferTable(${table.id},'${table.type_table}${table.number}')">${table.type_table}${table.number}</text>`);
                        }
                        else{
                            available = "#FF0000";
                             map.insertAdjacentHTML('beforeend',`<rect x=${map.width.baseVal.value*j/cols+1} y=${map.height.baseVal.value*i/rows} width=${size} height=${size} style="fill:${available}" onclick="void(0)"></rect>
            <text x=${map.width.baseVal.value*j/cols+40} y=${map.height.baseVal.value*i/rows+50} font-family="Verdana"
        font-size="20" onclick="void(0)">${table.type_table}${table.number}</text>`);
                        }
                }
                else break;
            }
        }


	});
    }
    else{alert('No hay ninguna mesa seleccionada');}
}
function transferTable(newTableID,newTable){

     // libera la mesa actual
       setTableFree();

    get("tickets/?is_closed=False&table=" + currentTableID, function(){
       // cambiar ticket de mesa
       var ticket = this.response[0];
       ticket.table = newTableID;
       put("tickets/"+ticket.pk+"/",function(){},ticket,true);

       //ocupar mesa nueva
        get("tables/"+newTableID+"/",function(){
           var table = this.response;
           table.is_available = false;
           put("tables/"+newTableID+"/",function(){
                                                    currentTableID = newTableID;
                                                    currentTable = newTable;
                                                    loadTPV();},table,true);
            });
    });
}

function loadTPV(){
	main.innerHTML = `<div class=" content container-fluid">
		<div class="row content">
		 <div class="col-sm-1 sidenav mappeat-sidenav" style="width: 12% ">
		     <div class="btn-group-vertical" style="width: 110%">
		     <button onclick="seeTables()" type="button" class="btn btn-primary btn-side" style="height: 70px">Ver Mesas</button>
		     <button type="button" class="btn btn-warning btn-side" style="height: 70px">Abrir Cajón</button>
   	     <button type="button" onclick='charge()' class="btn btn-success btn-side" style="height: 70px">Efectivo <span id="cashButton" class="badge">0€</span></button>
		     <button onclick="splitTicket()" type="button" class="btn btn-primary btn-side" style="height: 70px">Dividir Ticket</button>
		     <button onclick="sendKitchen()" type="button" class="btn btn-basic btn-side" style="height: 70px">Enviar a Cocina</button>
		     <button onclick="viewTables()" type="button" class="btn btn-warning btn-side" style="height: 70px">Transferir Mesa</button>
		     <button onclick="printTicket()" type="button" class="btn btn-info btn-side" style="height: 70px">Imprimir Ticket</button>
		     <button onclick="cancelTicket()" type="button" class="btn btn-danger btn-side" style="height: 70px">Cancelar Ticket</button>
		     </div><br>
		 </div>
		 <br>
		 <div class="col-sm-10">
		   <div class="row">
		     <div class="col-sm-8">
		       <div class="well">
		         <h4>Familias</h4>
		         <ul id="familiesList" class="ul-tpv">Cargando...</ul>
		       </div>
		     </div>
		     <div class="col-sm-4">
		       <div class="well">
		         <h4>Contexto Actual</h4>
		         <p>Camarero: ${sessionStorage['username']}</p>
		         <p id="tableName">Número de Mesa</p>
		         <p id="ticketID">Número de Ticket</p>
		       </div>
		     </div>
		   </div>
		   <div class="row">
		     <div class="col-sm-8">
		       <div class="well">
		         <h4>Productos</h4><button class='pull-right btn btn-warning btn-lg' onclick='toggleCombined()' id='combinedButton'>Combinar</button>
		         <ul id="productsList" class="ul-tpv">Cargando...</ul>

					 </div>
					 <!---
					   <div class="well">
		         <h4> Sugerencias de productos </h4>
		         <p> Aqui aparece una lista de productos de varias familias que tienen una gran probabilidad de ser incluídos en el ticket</p>
		       </div>
					 -->
		     </div>
		     <div class="col-sm-4">
		       <div id="ticketDiv" class="well">
                 <div class='text-center'>
		         <h4  id='ticketTitle'>Ticket Actual</h4>
                 <h4 id='ticketRest'>${sessionStorage['restaurantName']}</h4>
                 <h5 id='RestInfo'></h5>
                 <p id='nif'> NIF: </p>
                 </div>
                 <p id='n_ticket'>Factura simplificada n: </p>
                
                 <p id='ticketTime'>Fecha:</p>
                 <p id='ticketBarman'>Camarero: ${sessionStorage['username']}</p>
                 <p id='ticketTableName'>Mesa: ${currentTable}</p>
		         <table class='table' id="ticketTable"></table>
                 </div>
                 <div>
                 <table class='table'  id='kitchenTicket'></table>
                 </div>
		       </div>
		     </div>
		   </div>
		 </div>
	</div>`;

	familyWanted = '';
    combined = false;
    loadTicket();
    
	get("families/", function(){
			"use strict";
			let list = document.getElementById('familiesList');
			list.innerHTML = '';

			for (let family of this.response){
				list.insertAdjacentHTML('beforeend', `<li class="li-tpv" onclick="loadFamily('${family.name}')">${family.name}</li>`);
			}
            list.insertAdjacentHTML('beforeend', `<li class="li-tpv" onclick="loadFamily('')">Todos</li>`);
	});

	get("products/", function(){
			"use strict";
			if (familyWanted == ''){
				let list = document.getElementById('productsList');
				list.innerHTML = '';

				for (let product of this.response){
					list.insertAdjacentHTML('beforeend', `<li class="li-tpv" onclick="addTicketDetail(${product.id})">${product.name}</li>`);
				}
			}
	});

	
}

function loadApp(){
	document.body.innerHTML = `<header>
	<nav id=mappeat-navbar class="navbar navbar-inverse">
	<div class="container">
		<div class="navbar-header">
		  <a id=mappeat-logo class="navbar-brand" href="#">Mappeat</a>
		</div>
			<div id=navbar-parent class="navbar-collapse collapse navbar-right center-block ">
				<div id=navbar-buttons>
					<button type="button" class="btn btn-light" onclick="loadStore()">Almacén</button>
					<button type="button" class="btn btn-light"onclick="loadMenu()">Menú</button>
					<button type="button" class="btn btn-light"onclick="loadTPV()">TPV</button>
                    <button type="button" class="btn btn-light" onclick="loadHistory()">Historial</button>
					<!--  Aun no lo implementamos
					<button>Informes</button>
					-->
					<button type="button" class="btn btn-light" onclick="loadSettings();loadTables()">Ajustes</button>
					<button type="button" class="btn btn-danger" onclick="location.reload()">Salir</button>
				</div>
			</div>
	</div>
	</nav>
	</header>
	<main>
	</main>`;

	main = document.querySelector('main');
	loadTPV();
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

	let pendingData = 2;

	post("login/", function(){
		get("restaurants/", function(){
			sessionStorage['restaurantID'] = this.response[0].id;
            sessionStorage['restaurantName'] = this.response[0].name;
			pendingData -= 1;
			if (pendingData == 0) loadApp();
		});

		get("users/?username=" + valores.username, function(){
		get("staff/?user=" + this.response[0].pk, function(){
			sessionStorage['userID'] = this.response[0].id;
            sessionStorage['username'] = this.response[0].first_name;
			pendingData -= 1;
			if (pendingData == 0) loadApp();
		});
		});
	}, valores, true, "/rest-auth/");

	return false;
}

function loadStore(){
    main.innerHTML = `<div class="row content container-fluid">
                        <div class="col-sm-1"></div>
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
                         <div class="col-sm-1"></div>
                     </div>`;

    let list = document.getElementById('storeList');
    get('inventory/',function(){
                        'user strict';

                        list.innerHTML='';

                        for(let table of this.response){
                            //evita llamadas con supply null
                            if(table.supply){
                                get('suplies/'+table.supply,function(){
                                    list.insertAdjacentHTML('beforeend',`<tr><td><button onclick='removeInventory(${table.id})' class="glyphicon glyphicon-remove btn-danger"></button></td><td>${this.response.name}</td><td>${this.response.mesure_unity}</td><td>${this.response.barcode}</td><td>${table.quantity}</td></tr>`);}
                                    );
                            }
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
                                                <label>Tamaño</label><input type='number' name='size'><br>
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
    valoresSupply.size = form.size.value;
    valoresSupply.category = 2; // La categoria 2 se corresponde a 'Articulo'

    valoresInventory.quantity = form.quantity.value;
    valoresInventory.restaurant = sessionStorage['restaurantID'];
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
      main.innerHTML = `<div class="row content container-fluid">
                        <div class="col-sm-12">
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
                        list.insertAdjacentHTML('beforeend',`<tr><td class="active"><h4>${product.name}</h4></td><td style="vertical-align:middle;"> <span onclick='editProductForm(${product.id})' data-toggle="modal" data-target="#modalEditProduct"  class="glyphicon glyphicon-pencil text-warning pull-left"></span></td><td></td><td style="vertical-align:middle;"><button onclick="removeProduct(${product.id},'${product.name}')" class="glyphicon glyphicon-remove btn-danger pull-right"></button></td></tr><tr><td><img class="img-rounded" src='' alt='icono${product.icon}'></td><td><div class='well' id='ingredients${product.id}'></div></td><td><p class="bg-primary text-white">${product.price_with_tax}€</p><p class='bg-danger'>${this.response.strTax}</p><p class='bg-success'>${product.price_as_complement_with_tax}€</p></td>
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
            get('suplies/'+ingredient.supply, function(){  frame.insertAdjacentHTML('beforeend',`<li class="list-group-item"><span class='glyphicon glyphicon-minus text-danger' onclick='removeIngredient(${ingredient.id})'></span>   ${this.response.name}</li>`);});
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
    valores.restaurant = sessionStorage['restaurantID'] ;
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

function removeProduct(product,product_name){
    if (confirm('¿Desea eliminar '+ product_name + ' ?')){
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

// Asume que hay un ticket creado
/*
function addTicketDetail(product){
    var valores = new Object();

    get("tickets/?is_closed=False&table=" + currentTableID, function(){
        valores.ticket = this.response[0].pk;
        valores.restaurant = this.response[0].restaurant;
        valores.product = product;
        valores.quantity = 1;
        // ?
        valores.isComplement = false;
        get("products/"+product,function(){
            valores.name = this.response.name;
            valores.price = this.response.price_with_tax;
            post("ticket_details/",function(){loadTicket();},valores,true);
        });

	});
}
*/

//Asume que hay un ticket creado
function addTicketDetail(product, quantity=1){
    var valores = new Object();
	valores.ticket = currentTicketID;
	valores.product = product;
	valores.quantity = quantity;
	valores.isComplement = combined;
    
	post("ticket_details/",function(){if(combined) toggleCombined();
                                      loadTicket();},valores,true);
}

function removeTicketDetail(id){
    _delete('ticket_details/'+id,function(){loadTicket();},true);
}

function sendKitchen(){
    if (currentTableID){
        get("tickets/?is_closed=False&table=" + currentTableID, function(){
            get("ticket_details/?ticket="+this.response[0].pk+"&sent_kitchen=False",function(){
                for(let line of this.response ){
                    line.sent_kitchen = true;
                    put('ticket_details/'+line.pk+'/',function(){},line,true);
                }
                printTicketKitchen();
                loadTPV();
            });
        });
    }
}

function printTicket(){
        var mode = 'iframe'; //popup
        var close = mode == "popup";
        var options = { mode : mode, popClose : close};
        $("#ticketDiv").print( options );
    
}

function printTicketKitchen(){
    var mode = 'iframe'; //popup
        var close = mode == "popup";
        var options = { mode : mode, popClose : close};
        $("#kitchenTicket").print( options );
}

function charge(){
    if(currentTableID){
    //abrir cajon
        // TODO

        get("tickets/?is_closed=False&table=" + currentTableID,function(){
                let ticket =this.response[0];
                //cierra el ticket
                ticket.is_closed = true;
                put("tickets/"+ ticket.pk +"/",function(){
                    setTableFree();
                    loadTPV();
                },ticket,true);
        });
    }
}

function setTableFree(){
     get('tables/'+currentTableID+'/',function(){
                var valores = this.response;
                valores.is_available = true;
                put('tables/'+currentTableID+'/',function(){
                                                currentTable = undefined;
                                                currentTableID = undefined;

                                                },valores,true)}
               );
}

function loadHistory(){
    main.innerHTML = `<div class="content row container-fluid">
                         <div class="col-sm-2"></div>
                      <div class='col-md-8 well'>
                        <ul class="list-group" id='ticketList'></ul>
                      </div>
                       <div class="col-sm-2"></div>
                      </div>`;

    // 'zh-Hans-CN' para obtener formato yyyy/mm/dd
    var today = new Date().toLocaleDateString('zh-Hans-CN');
    // cambia / por -
    var currentDate = today.replace(new RegExp('/', 'g'),'-');

    get("tickets/?is_closed=True&date="+currentDate,function(){

       var list = document.getElementById('ticketList');
       list.innerHTML='';

       for( var ticket of this.response){
           list.insertAdjacentHTML('beforeend',`<li  class="list-group-item" onclick='seeTicket(${ticket.pk})'>${ticket.time}<span class='pull-right'>${ticket.cost.toFixed(2)}€</span></li>`);
       } 
    });
}

function seeTicket(ticket){
     main.innerHTML = `<div class="row content container-fluid">
                        <div class="btn-toolbar" role="toolbar">
                            <button type="button" class="btn btn-default btn-lg"  onclick='loadTPV()'>
                            <span class='glyphicon glyphicon-arrow-left'></span>
                            </button>
                            <h3 class="text-center"></h3>
                        </div>
                       <div class='col-md-2 '></div>
                      <div class='col-md-8 well'>
                        <div id="ticketDiv" class="well">
                          <div class='text-center'>
                            <h4 id='ticketRest'>${sessionStorage['restaurantName']}</h4>
                            <h5 id='RestInfo'></h5>
                            <p id='nif'> NIF: </p>
                          </div>
                          <p id='n_ticket'>Factura simplificada n: </p>
                          <p id='ticketTime'>Fecha:</p>
                          <p id='ticketBarman'>Camarero: </p>
                          <p id='ticketTableName'>Mesa: </p>
		                  <table class='table' id="ticketTable"></table>
                        </div>
                         <div class='text-center'>
                         <button class='btn btn-success btn-lg' onclick='printTicket()'>Imprimir Ticket</button>
                        </div>
                      </div>
                       <div class='col-md-2 '></div>

                      </div>`;
    
    
    
    get('tickets/'+ticket+'/',function(){
        
        var total_without_tax = 0.0;
        var table = document.getElementById('ticketTable');
        var ticket = this.response;
        
        get ('restaurants/'+ticket.restaurant+'/',function(){
            var rest = this.response;
            document.getElementById('RestInfo').innerText = rest.address +"  "+rest.city;
            document.getElementById('nif').insertAdjacentHTML('beforeend',rest.nif);
        });
        
        document.getElementById('ticketTime').insertAdjacentHTML('beforeend',`${ticket.time}  ${ticket.date}`);
        document.getElementById('n_ticket').insertAdjacentHTML('beforeend',`${ticket.pk}`);
        
        table.innerHTML = `<thead>
		                      <tr>
                                <th class='text-center'>Cantidad</th>
			                    <th class='text-center'>Producto</th>
			                    <th class='text-center'>Precio Unidad</th>
			                    <th class='text-center'>Importe</th>
		                      </tr>
	                       </thead>
	                       <tbody>
	                       </tbody>
                           <tfoot id='totalTicket'>
                           <tr><td></td><td><strong>SubTotal:</strong><td></td><td id='subtotal'></td></tr>
                           <tr><td></td><td><strong>Total:</strong><td></td><td><strong>${ticket.cost.toFixed(2)}€</strong></td></tr>
                           </tfoot>`;
	table = table.lastChild;
        
    for (let line of ticket.details){
          get('products/'+line.product+'/',function(){
            var product = this.response;
            get('iva/'+product.iva_tax+'/',function(){
                total_without_tax += line.quantity*product.price_with_tax*(1-(this.response.tax/100));
                table.insertAdjacentHTML('afterbegin', `<tr onclick="void(0)">
			<td class='text-center'>${line.quantity}</td>
            <td class='text-center'>${line.product_name}</td>
			<td class='text-center'>${line.price.toFixed(2)}€</td>
            <td class='text-center'>${(line.price*line.quantity).toFixed(2)}€</td>
		    </tr>`);
                document.getElementById('subtotal').innerHTML=`<strong>${total_without_tax.toFixed(2)}€</strong>`;
                });
            });
    }
        
    });
    
    
}

function toggleCombined(){
    button = document.getElementById('combinedButton');
    if(combined){
        combined = false;
        button.style.filter = "none";
    }
    else{
        combined = true;
        button.style.filter = "grayscale(100%)";
       
    }
}

function showCalculator(id){
    currentTicketDetailID = id;
    main.insertAdjacentHTML('beforeend',`<div class="modal fade" id="modalCalc" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	                                       <div class="modal-dialog" role="document">
		                                      <div class="modal-content">
			                                     <div class="modal-header">
				                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
					                               <span aria-hidden="true">&times;</span></button>
				                                    <h4 class="modal-title" id="myModalLabel">Editar</h4>
			                                     </div>
			                                 <div class="modal-body">
                                                <form onsubmit='return editTicketDetail()'>
                                                
                                                <div id="calculator">
	                                            <div class="top">
		                                          <div class="screen" id='screenCalc' name='screenCalc'></div>
	                                               </div>
	                                            <div class="keys">
		                                          <span onclick='addCalc(7)'>7</span>
		                                          <span onclick='addCalc(8)'>8</span>
		                                          <span onclick='addCalc(9)'>9</span>
		                                          <span onclick='addCalc(4)'>4</span>
		                                          <span onclick='addCalc(5)'>5</span>
		                                          <span onclick='addCalc(6)'>6</span>
		                                          <span onclick='addCalc(1)'>1</span>
		                                          <span onclick='addCalc(2)'>2</span>
		                                          <span onclick='addCalc(3)'>3</span>
		                                          <span onclick='addCalc(0)'>0</span>
		                                          <span onclick='addCalc(".")'>.</span>
                                                  <span onclick='addCalc("C")' class="clear">C</span>
	                                           </div>
                                            </div>
                                            <div class="modal-footer">
                                                <button type='submit' class='btn-success btn pull-right'>Continuar</button>
                                            </div>
                                            </div>
                                            </form>
			                             </div></div></div></div>`);
    document.getElementById('screenCalc').innerHTML='';
    $('#modalCalc').modal('show');
    
    
}

function addCalc(n){
    if(n =='C')
        document.getElementById('screenCalc').innerHTML='';
    else
        document.getElementById('screenCalc').innerHTML=document.getElementById('screenCalc').innerHTML+n;
}

function editTicketDetail(){
    var valores = new Object();
    get('ticket_details/'+currentTicketDetailID +'/', function(){ valores = this.response;
                                              valores.price =document.getElementById('screenCalc').innerHTML;
                                              put('ticket_details/'+currentTicketDetailID+'/', function(){ $('#modalCalc').modal('hide');
                                                                                        loadTicket();}, valores);
                                              
                
                                              });
    
       return false;
    
}