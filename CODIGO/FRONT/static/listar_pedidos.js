// Define una variable global baseUrl que contiene el inicio de la URL
const baseUrl = `${window.location.protocol}//${window.location.host}`;

function cargarDatos() {
  // Obtiene el ID del alumno de la cookie
  var idAlumno = getCookie('id_alumno');
  idAlumno = parseInt(idAlumno);

  if (idAlumno) {
    // Obtiene los pedidos asociados al ID del alumno
    fetch(`${baseUrl}/cafeteria/pedidos?id_alumno=${idAlumno}`)
      .then(response => response.json())
      .then(data => {
        console.log(data);
        mostrarPedidos(data);
      });
  } else {
    console.log('No se encontró el ID del alumno en la cookie.');
  }
}

// Llamamos a cargarDatos al cargar la página
window.onload = function() {
  let x = document.cookie;
  if (!x.includes("correo")) {
    alert("Debes iniciar sesión para acceder a esta página.");
    window.location.replace("/");
  }
  cargarDatos();
};

// Función que recibe el JSON y muestra los pedidos en la página
function mostrarPedidos(data) {
    var pedidos = data.data;
    var html = '';
  
    if (pedidos.length > 0) {
      for (var i = 0; i < pedidos.length; i++) {
        var id_pedido = `Pedido ${pedidos[i].id_pedido}`;
        var lista_productos = `Pedido ${pedidos[i].productos_ids}`;
        for (var j= 0; j<lista_productos;i++){
            var nombre_producto = `Pedido ${pedidos[i].productos_descripciones[j]}`;
  
            html += `
            <div class="pedido">
                <button class="btn btn-primary" onclick="verDetallesPedido('${pedidos[i].id_pedido}')">
                ${id_pedido} | ${nombre_producto}
                </button>
            </div>
            <br>
            `;
        }
      }
    } else {
      html = '<h2 style="color:red">No tienes ningún pedido.</h2>';
    }
  
    document.getElementById('pedidos').innerHTML = html;
  }
  

// Función que redirige a la página de detalles del pedido seleccionado
function verDetallesPedido(idPedido) {
  // Redirigir a la página que muestra los detalles del pedido con el ID especificado
  window.location.href = `/cafeteria/detalles_pedido/${idPedido}`;
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
