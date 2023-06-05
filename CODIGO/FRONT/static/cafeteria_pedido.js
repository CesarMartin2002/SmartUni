// Define una variable global baseUrl que contiene el inicio de la URL
const baseUrl = `${window.location.protocol}//${window.location.host}`;
var filtro = "";
const id_alumno = getCookie('id_alumno');
var cantidades = new Map();
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
    if (!cantidades.has(productos[i].id_producto))
    cantidades.set(productos[i].id_producto, 0);

    html += `
    <div class="cantidad-prod">
      <div class="producto">
        <button class="btn btn-minus" onclick="restarCantidad(${productos[i].id_producto})">-</button>
        <button class="btn btn-primary" onclick="window.location.href = 'productos/${productos[i].id_producto}'">
          ${nombre} | ${precio}
        </button>
        <button class="btn btn-plus" onclick="sumarCantidad(${productos[i].id_producto})">+</button>
      </div>
      <p class="cantidad" id="cantidad${productos[i].id_producto}">Cantidad: ${cantidades.get(productos[i].id_producto)}</p>
    </div>
      <br>
    `;
    document.getElementById('productos').innerHTML = html;


  }

}

// Funciones para restar y sumar la cantidad de productos
function restarCantidad(idProducto) {
  console.log("restar cantidad");
  console.log(idProducto);
  if (cantidades.get(idProducto) > 0) {
    cantidades.set(idProducto, cantidades.get(idProducto) - 1);
  }
  document.getElementById(`cantidad${idProducto}`).innerHTML = `Cantidad: ${cantidades.get(idProducto)}`;
  // Implementa la lógica para restar la cantidad del producto con el id proporcionado
}

function sumarCantidad(idProducto) {
  console.log("sumar cantidad");
  console.log(idProducto);
  cantidades.set(idProducto, cantidades.get(idProducto) + 1);
  document.getElementById(`cantidad${idProducto}`).innerHTML = `Cantidad: ${cantidades.get(idProducto)}`;
  // Implementa la lógica para sumar la cantidad del producto con el id proporcionado
}

//funcion para obtener el producto estrella de la cafeteria:
function productoEstrella(){
  ruta= `/cafeteria/pedidos/estrella`;
  rutaAlumno = `/cafeteria/pedidos/estrella?id_alumno=${id_alumno}`;
  console.log(ruta);
  fetch(ruta)
    .then(response => {
      if (response.status == 404) {
        document.getElementById('productoAlumno').style.display = 'none';
        return;
        // throw new Error("No hay pedidos");
      }
      if (response.ok) {
        return response.json();
      }
    })
    .then(data => {
      console.log(data);
      // mostrarEstrella(data);
      var producto = data.data;
      var nombre = producto.descripcion;
      // var idProducto = `Id producto => ${producto.id_producto}`;
      // var cantidad = `Nº de veces que se ha pedido =>${producto.cantidad}`;
      var html = document.getElementById('productoEstrella').innerHTML;
      
      var html = html+`
          <h3>${nombre}</h3>
          <br>

      `;
      
      document.getElementById('productoEstrella').innerHTML = html;
      
    }
    )
    fetch(rutaAlumno)
    .then(response => {
      if (response.status == 404) {
        throw new Error("El alumno no ha realizado pedidos aun, por ende no se le puede mostrar ninguna recomendacion.");
      }
      if (response.ok) {
        return response.json();
      }
    })
    .then(data => {
      var producto = data.data;
      var nombre = producto.descripcion;
      var html = document.getElementById('productoAlumno').innerHTML;
  
      var html = html+`
          <h3>${nombre}</h3>
          <br>
      `;
  
      document.getElementById('productoAlumno').innerHTML = html;
    })
    .catch(error => {
      document.getElementById('productoAlumno').style.display = 'none';
      console.error(error);
    });
  
}

// Función para crear un pedido
function crearPedido() {
  var productos = [];
  for (let [key, value] of cantidades) {
    if (value > 0) {
      for (let i = 0; i < value; i++) {
        productos.push(key);
      };
    }
  }
  if (productos.length == 0) {
    alert("No hay productos seleccionados");
    return;
  }

  json = {
    "id_alumno": id_alumno,
    "productos": productos
  }

  var url = `/cafeteria/pedidos`;
  var data = JSON.stringify(json);
  console.log(data);
  fetch(url, {
    method: 'POST',
    body: data,
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      alert("Pedido realizado correctamente. El id de su pedido es: " + data.data.id_pedido + ".");
      window.location.href = '/cafeteria/mis_pedidos';
    }
    )
    .catch(error => {
      console.error(error);
      // Aquí puedes realizar acciones adicionales en caso de error.
    }
    );


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