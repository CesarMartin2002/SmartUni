
window.onload= function(){
    let x = document.cookie;
    if(!x.includes("correo")){
        alert("Debes iniciar sesión para acceder a esta página.");
        window.location.replace("/");

    }
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

  // Función para obtener la información de la taquilla reservada del alumno
function obtenerInformacionTaquillaReservada(idAlumno) {
    return fetch(`/taquilla/Alumno/${idAlumno}`)
      .then(response => response.json())
      .then(data => {
        if (data.code === 200) {
          return data.data; // la información de la taquilla reservada se encuentra en data.data
        } else {
          return null; // No se encontró una taquilla reservada para el alumno
        }
      });
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

// Función para obtener si el alumno tiene una taquilla reservada
async function obtenerTaquillaReservada() {
    // para redirigir a la página 'taquillas.html', puedes usar:
    // Obtiene los valores de las taquillas generando un botón con la información de cada una
    var taquillaDeAlumno = await obtenertaquillaDeAlumno();
    taquillaDeAlumno = taquillaDeAlumno[0];
    if (taquillaDeAlumno) {
        console.log(taquillaDeAlumno);
        window.location.href = `/detalleTaquilla/${taquillaDeAlumno.id_taquilla}`;
    } else {
        window.location.href = '/lockers';
    }
}