//Obtenemos la url base del sitio
const baseUrl = `${window.location.protocol}//${window.location.host}`;
var estado = 0;
const id_alumno = parseInt(getCookieValue("id_alumno"));


//funcion que se ejecuta al cargar la pagina
window.onload = function () {
  let x = document.cookie;
  if (!x.includes("correo")) {
    alert("Debes iniciar sesión para acceder a esta página.");
    window.location.replace("/");
  } else {
    obtenerDetallePedido(); // Llamada para obtener el detalle del pedido al cargar la página
  }
};


//obtenemos los elementos del DOM que vamos a utilizar
const btnScan = document.getElementById("scan-btn");
const btnSimulateScan = document.getElementById("simulate-scan-btn");
const btnAvanzar = document.getElementById("avanzar-btn");

//agregamos los eventos a los botones
btnScan.addEventListener("click", escaneoReal);
btnSimulateScan.addEventListener("click", escaneoSimulado);
btnAvanzar.addEventListener("click", avanzar);


// función para obtener el detalle del pedido
function obtenerDetallePedido() {
  // obtenemos el ID del pedido
  const idPedido = getLastPathParameter();
  
  // construimos la URL para obtener el detalle del pedido
  const url = `${baseUrl}/cafeteria/pedidos/${idPedido}`;

  // realizamos la petición GET para obtener el detalle del pedido
  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Error al obtener el pedido');
      }
      return response.json();
    })
    .then(data => {
      // mostramos los datos del pedido
      mostrarDetallePedido(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// función para mostrar el detalle del pedido
function mostrarDetallePedido(data) {
  var pedido = data.data;
  var idPedido = `Pedido <span class="negrita">${pedido.id_pedido}</span>`;
  var correoAlumno = `<li><span class="negrita">Correo del alumno => </span>${pedido.correo_alumno}</li>`;
  var productos = '';

  for (var j = 0; j < pedido.productos_ids.length; j++) {
    //var productoId = pedido.productos_ids[j];
    var productoDescripcion = pedido.productos_descripciones[j];
    productos += `<li><span class="negrita">Nombre producto => </span> ${productoDescripcion}</li>`;
  }
  estado = pedido.estado;
  var estadoHtml = '';
  if (estado == 0){
    estadoHtml = `<li id="estado"><span class="negrita">Estado => </span>✅ - Aprobación pendiente</li>`;
  }else if (estado == 1){
    estadoHtml = `<li id="estado"><span  class="negrita">Estado => </span>🧑‍🍳 - Preparando en cocina</li>`;
  }else if (estado == 2){
    estadoHtml = `<li id="estado"><span  class="negrita">Estado => </span>👜 - Listo para recoger</li>`;
  }else if (estado == 3){
    estadoHtml = `<li id="estado"><span class="negrita">Estado => </span>🍽️ - Consumiendo</li>`;
  }else if (estado == 4){
    estadoHtml = `<li id="estado"><span class="negrita">Estado => </span>😀 - Finalizado</li>`;
  }
  else{
    estadoHtml = `<li id="estado"><span class="negrita">Estado => </span>❌ - Cancelado</li>`;
  }
  

  var html = `
    <div class="detallepedido">
      <h2>${idPedido}</h2>
      <ul>${correoAlumno}</ul>
      <ul>${productos}</ul>
      <ul>${estadoHtml}</ul>
    </div>
    <br>
  `;

  document.getElementById('pedidos').innerHTML = html;
}





//funcion que se ejecuta al escanear un nfc la pagina
async function scanNFC() {
  try {
    return new Promise((resolve, reject) => {
      //creamos un nuevo lector de nfc
      const ndef = new NDEFReader();
      //iniciamos el escaneo
      ndef.onreading = event => {
        const serialNumber = event.serialNumber;
        console.log(`> Serial Number: ${serialNumber}`);
        resolve(serialNumber);
      };
      //si hay un error al leer la tarjeta
      ndef.onreadingerror = () => {
        console.error("No se puede leer la tarjeta NFC. ¿Intentar con otra?");
        document.getElementById("header-info").innerHTML = "No se puede leer la tarjeta NFC. ¿Intentar con otra?";
        reject(null);
      };
      ndef.scan();
    });
  } catch (error) {
    console.error("Error al iniciar el escaneo NFC:", error);
    document.getElementById("header-info").innerHTML = "Error al iniciar el escaneo NFC: " + error.message;
    return null;
  }
}


async function escaneoReal(){
  var ncf = await scanNFC();
  console.log(ncf);
  if (ncf != null){
    ncf = ncf.toString();
    // document.getElementById("header-info").innerHTML = ncf;
    consultarPedidoNfc(ncf);

  }
}

function escaneoSimulado(){
  const ncf = "123456789";
  // document.getElementById("header-info").innerHTML = ncf;
  consultarPedidoNfc(ncf);
}

function actualizarEstado(){
  if (estado == 0){
    estadoHtml = `<span class="negrita">Estado => </span>✅ - Aprobación pendiente`;
  }else if (estado == 1){
    estadoHtml = `<span class="negrita">Estado => </span>🧑‍🍳 - Preparando en cocina`;
  }else if (estado == 2){
    estadoHtml = `<span class="negrita">Estado => </span>👜 - Listo para recoger`;
  }else if (estado == 3){
    estadoHtml = `<span class="negrita">Estado => </span>🍽️ - Consumiendo`;
  }else if (estado == 4){
    estadoHtml = `<span class="negrita">Estado => </span>😀 - Finalizado`;
  }
  else {
    estadoHtml = `<span class="negrita">Estado => </span>❌ - Cancelado`;
  }
  document.getElementById("estado").innerHTML = estadoHtml;
}

function avanzar(){
  if (estado == 4){
    return;
  }
  const idPedido = parseInt(getLastPathParameter());
  const url = `${baseUrl}/cafeteria/pedidos/${idPedido}`;
  const data = {
    estado: estado + 1,
    id_alumno: id_alumno
  };

  fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => {
      if (response.ok) {
        estado = estado + 1;
        actualizarEstado();
      }
    })
    .catch(error => {
      console.error('Error:', error);
    }
  );

  
}

function consultarPedidoNfc(nfc) {
  //el id del pedido se obtiene de la url de la pagina pasandolo a int
  const idPedido = parseInt(getLastPathParameter());
  const url = `${baseUrl}/cafeteria/pedidos/nfc/${idPedido}`;
  const data = {
    num_serie: nfc,
    id_alumno: id_alumno,
    estado: 3
  };

  fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => {
      if (response.ok) {
        document.getElementById("header-info").innerHTML = "Verificación exitosa.";
        //cambiamos en el css el color de la variable en root llamada --main-bg a #58e76b
        document.documentElement.style.setProperty('--main-bg', '#58e76b');
        //ocultamos el boton de escanear
        document.getElementById("scan-btn").style.display = "none";
        //ocultamos el boton de simular escaneo
        document.getElementById("simulate-scan-btn").style.display = "none";
        estado = 3;
        document.getElementById("estado").innerHTML = "🍽️ - Consumiendo";
      } else {
        document.getElementById("header-info").innerHTML = "Verificación fallida.";
        //cambiamos en el css el color de la variable en root llamada --main-bg a #e75858
        document.documentElement.style.setProperty('--main-bg', '#e75858');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
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

function getCookieValue(name) {
  const cookies = document.cookie.split(";").map((cookie) => cookie.trim());
  for (const cookie of cookies) {
    if (cookie.startsWith(name + "=")) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

function getLastPathParameter() {
  const path = window.location.pathname;
  const pathSegments = path.split("/");
  return pathSegments[pathSegments.length - 1];
}

async function sendPutRequest(idPedido, data) {
  const url = `${baseUrl}/cafeteria/pedidos/nfc/${idPedido}`;

  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    return response;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}
