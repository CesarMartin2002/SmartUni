// Define una variable global baseUrl que contiene el inicio de la URL
const baseUrl = `${window.location.protocol}//${window.location.host}`;
var filtro = "";
const id_alumno = getCookie('id_alumno');
function cargarDatos(){
  //obtiene los valores de los records generando un boton con la informacion de cada uno
  filtro = document.getElementById("input").value;
  if (filtro == undefined) filtro = "";
  ruta= `${baseUrl}/cafeteria/productos?filtro=${filtro}`;
  console.log(ruta);
  fetch(ruta)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      mostrarDatos(data);
      
    }
    )
}
//llamamos a cargarDatos al cargar la pagina
window.onload = productoEstrella();
window.onload = cargarDatos();

//funcion que recibe el json y lo muestra en la pagina
function mostrarDatos(data) {
  var productos = data.data;
  var html = '';
  
  for (var i = 0; i < productos.length; i++) {
    nombre = productos[i].descripcion;
    precio = productos[i].precio;
    
    html += `
      <div class="producto">
        <button class="btn btn-minus" onclick="restarCantidad(${productos[i].id_producto})">-</button>
        <button class="btn btn-primary" onclick="window.location.href = 'productos/${productos[i].id_producto}'">
          ${nombre} | ${precio}
        </button>
        <button class="btn btn-plus" onclick="sumarCantidad(${productos[i].id_producto})">+</button>
      </div>
      <br>
    `;
  }
  
  document.getElementById('productos').innerHTML = html;
}

// Funciones para restar y sumar la cantidad de productos
function restarCantidad(idProducto) {
  console.log("restar cantidad");
  console.log(idProducto);
  // Implementa la lógica para restar la cantidad del producto con el id proporcionado
}

function sumarCantidad(idProducto) {
  console.log("sumar cantidad");
  console.log(idProducto);
  // Implementa la lógica para sumar la cantidad del producto con el id proporcionado
}

//funcion para obtener el producto estrella de la cafeteria:
function productoEstrella(){
  ruta= `/cafeteria/pedidos/estrella`;
  rutaAlumno = `/cafeteria/pedidos/estrella?id_alumno=${id_alumno}`;
  console.log(ruta);
  fetch(ruta)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // mostrarEstrella(data);
      var producto = data.data;
      var nombre = producto.descripcion;
      var idProducto = `Id producto => ${producto.id_producto}`;
      var cantidad = `Nº de veces que se ha pedido =>${producto.cantidad}`;
      var html = '';
      
      var html = `
        <div class="detallepedido">
          <ul>${nombre}</ul>
          <ul>${idProducto}</ul>
          <ul>${cantidad}</ul>
        </div>
        <br>
      `;
      
      document.getElementById('productoEstrella').innerHTML = html;
      
    }
    )
  fetch(rutaAlumno)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      var producto = data.data;
      var nombre = producto.descripcion;
      var idProducto = `Id producto => ${producto.id_producto}`;
      var cantidad = `Nº de veces que se ha pedido =>${producto.cantidad}`;
      var html = '';
      
      var html = `
        <div class="detallepedido">
          <ul>${nombre}</ul>
          <ul>${idProducto}</ul>
          <ul>${cantidad}</ul>
        </div>
        <br>
      `;
      
      document.getElementById('productoAlumno').innerHTML = html;
      
    }
    )
}

// Función para obtener el valor de una cookie por su nombre
function getCookie(name) {
  var cookieName = name + '=';
  var decodedCookie = decodeURIComponent(document.cookie);
  var cookieArray = decodedCookie.split(';');

  for (var i = 0; i < cookieArray.length; i++) {
    var cookie = cookieArray[i];
    while (cookie.charAt(0) === ' ') {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(cookieName) === 0) {
      return cookie.substring(cookieName.length, cookie.length);
    }
  }

  return '';
}