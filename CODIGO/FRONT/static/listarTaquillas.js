// Define una variable global baseUrl que contiene el inicio de la URL
const baseUrl = `${window.location.protocol}//${window.location.host}`;
var hola;

async function cargarDatos() {
  // Obtiene los valores de las taquillas generando un botón con la información de cada una
  var taquillaDeAlumno = await obtenertaquillaDeAlumno();
  taquillaDeAlumno = taquillaDeAlumno[0];
  hola = taquillaDeAlumno;
  if (taquillaDeAlumno) {
    console.log(taquillaDeAlumno);
    // Mostrar la taquilla reservada del alumno
    mostrarTaquillaReservada(taquillaDeAlumno);
  } else {
    // Mostrar todas las taquillas disponibles
    fetch(`${baseUrl}/taquillas?ocupado=false`)
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if (data.data.length > 0) {
          mostrarDatos(data);
        } else {
          var mensaje = 'No hay taquillas disponibles en este momento.';
          document.getElementById('taquillas').innerHTML = `<p>${mensaje}</p>`;
        }
      })
      .catch(error => {
        console.error(error);
      });
  }
}

// Llamamos a cargarDatos al cargar la página
window.onload = cargarDatos;

// Función para mostrar la taquilla reservada del alumno
function mostrarTaquillaReservada(taquillaDeAlumno) {
  console.log(taquillaDeAlumno);
  var html = `
    <div class="taquilla">
      <button class="btn btn-primary" onclick="window.location.href = '/taquillas/${taquillaDeAlumno.id_taquilla}'">
        Taquilla Reservada (${taquillaDeAlumno.id_taquilla})
      </button>
      <button class="btn btn-danger" onclick="cancelarReserva(${taquillaDeAlumno.id_taquilla})">
        Cancelar Reserva
      </button>
    </div>
    <br>
  `;

  document.getElementById('taquillas').innerHTML = html;
}

// Función que recibe el JSON y muestra las taquillas en la página
//Se entra aquí si no hay taquilla reservada y se muestran todas las taquillas disponibles
function mostrarDatos(data) {
  var taquillas = data.data;
  var html = '';

  for (var i = 0; i < taquillas.length; i++) {
    var numero_taquilla = `Taquilla ${taquillas[i].id_taquilla}`;

    html += `
      <div class="taquilla">
        <button class="btn btn-primary" onclick="window.location.href = '/taquillas/${taquillas[i].id_taquilla}'">
          ${numero_taquilla}
        </button>
      </div>
      <br>
    `;
  }

  document.getElementById('taquillas').innerHTML = html;
}

// Función para obtener el ID del alumno reservado
async function obtenertaquillaDeAlumno() {
  // Obtener el ID del alumno del local storage o de las cookies, según sea el caso
  var idAlumno = getCookie('id_alumno');
  //convertimos a entero idAlumno
  idAlumno = parseInt(idAlumno);

  // Verificar si se obtuvo el ID del alumno
  if (idAlumno) {
    // Lógica para obtener la información de la taquilla reservada para el alumno con el ID obtenido
    return obtenerInformacionTaquillaReservada(idAlumno)
      .then(taquillaReservada => {
        if (taquillaReservada) {
          // El alumno tiene una taquilla reservada
          return taquillaReservada;
        } else {
          // No se encontró una taquilla reservada para el alumno
          return false;
        }
      })
      .catch(error => {
        console.error(error);
        return false;
      });
  }

  // El alumno no tiene una taquilla reservada o no se encontró el ID del alumno
  return false;
}

// Función para obtener la información de la taquilla reservada del alumno
function obtenerInformacionTaquillaReservada(idAlumno) {
  return fetch(`${baseUrl}/taquilla/Alumno/${idAlumno}`)
    .then(response => response.json())
    .then(data => {
      if (data.code === 200) {
        return data.data; // Supongamos que la información de la taquilla reservada se encuentra en data.data
      } else {
        return null; // No se encontró una taquilla reservada para el alumno
      }
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
