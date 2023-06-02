
window.onload= function(){
    let x = document.cookie;
    if(!x.includes("correo")){
        alert("Debes iniciar sesión para acceder a esta página.");
        window.location.replace("/");

    }
    cargarDatos();
}
const btnMenu = Array.from(document.querySelectorAll('.btn-menu'));


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

function getCookieValue(name) {
  const cookies = document.cookie.split(";").map((cookie) => cookie.trim());
  for (const cookie of cookies) {
    if (cookie.startsWith(name + "=")) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

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

function getLastPathParameter() {
    const path = window.location.pathname;
    const pathSegments = path.split("/");
    return pathSegments[pathSegments.length - 1];
  }

async function cargarDatos(){
    id=parseInt(getLastPathParameter()); 
    fetch(`/taquillas/${id}`)
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

function mostrarDatos(data) {
    var taquilla = data.data;
    var taquilla = taquilla[0]
    console.log(taquilla);
    var html = '';
    var num_taquilla = `Taquilla número ${taquilla.id_taquilla}`;
    var pass_taquilla = `Contraseña: ${taquilla.password}`;
    var ala_taquilla = `Ala: ${taquilla.ala}`;
    var piso_taquilla = `Piso: ${taquilla.piso}`;
    var pasillo_taquilla = `Pasillo: ${taquilla.piso}`;
    var reservar_taquilla = taquilla.ocupado ? 'CANCELAR TAQUILLA' : 'SOLICITAR TAQUILLA';
    var buttonFunction = taquilla.ocupado ? `cancelarTaquilla(${taquilla.id_taquilla})` : `reservarTaquilla(${taquilla.id_taquilla})`;
    var titulo = taquilla.ocupado ? 'MI TAQUILLA' : 'RESERVAR TAQUILLA';

    if(taquilla.ocupado){
      html += `
        <div class="taquilla">
        <h1>${titulo}</h1>
        <h2>${num_taquilla}</h2> 
        <h2>${pass_taquilla}</h2>  
        <h2>${ala_taquilla}</h2>
        <h2>${piso_taquilla}</h2> 
        <h2>${pasillo_taquilla}</h2>
        <button id= i class="btn btn-primary" onclick="${buttonFunction}">
          ${reservar_taquilla}
        </button>
        </div>
      `;
    }
    else{
      html += `
        <div class="taquilla">
        <h2>${num_taquilla}</h2>    
        <h2>${ala_taquilla}</h2>
        <h2>${piso_taquilla}</h2> 
        <h2>${pasillo_taquilla}</h2>
        <button id= i class="btn btn-primary" onclick="${buttonFunction}">
          ${reservar_taquilla}
        </button>
        </div>
      `;
    }

    
    
    document.getElementById('taquillas').innerHTML = html;
}



function reservarTaquilla(idTaquilla) {
  const url = `/taquillas/reservar/${idTaquilla}`;
  const idAlumno = parseInt(getCookieValue("id_alumno"));
  const data = {
    id_alumno: idAlumno
  };

  console.log(idAlumno)

  fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => {
      if (response.ok) {
        console.log('Se ha reservado la taquilla con éxito');
        window.location.reload(); // Recargar la página
      } else {
        console.log('No se ha reservado la taquilla :(');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function cancelarTaquilla(idTaquilla) {
  const idAlumno = parseInt(getCookieValue("id_alumno"));
  const url = `/taquillas/cancelar/${idTaquilla}/${idAlumno}`;

  fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    }  
  })
    .then(response => {
      if (response.ok) {
        console.log('Se ha cancelado la reserva de la taquilla');
        window.location.href = '/lockers'; // Nos lleva a la página de taquillas
      } else {
        console.log('No se ha cancelado la taquilla :(');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function mostrarMensaje(mensaje) {
  const mensajeElement = document.getElementById('mensaje');
  mensajeElement.innerText = mensaje;
}
