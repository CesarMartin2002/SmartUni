
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

function cargarDatos(){
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
    console.log(taquilla);
    var html = '';
    html += `
        
      `;
    
  
    document.getElementById('taquillas').innerHTML = html;
}



