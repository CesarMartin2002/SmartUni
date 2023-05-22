
// Define una variable global baseUrl que contiene el inicio de la URL
const baseUrl = `${window.location.protocol}//${window.location.host}`;

  function imprimirArgumento(arg) {
    console.log(arg);
  }



function registrarse(user, pass, rpass) {

console.log("Usuario " + user + " y contraseña " + pass + " y repite contraseña " + rpass);
        //call a java servlet (url GetInicioSesion) that logs in with user.value and pass.value
        if (pass != rpass) {    
            console.log("Las contraseñas no coinciden");
            document.getElementById("errorMsg").innerHTML = "Las contraseñas no coinciden";
            document.getElementById("errorMsg").style.display = 'block';
            return;
        }
        if (user == "" || pass == "" || rpass == "") {
          console.log("Debes rellenar todos los campos");
          document.getElementById("errorMsg").innerHTML = "Debes rellenar todos los campos";
          document.getElementById("errorMsg").style.display = 'block';
          return;
        }
        if (!validarCorreoElectronico(user)) {
          console.log("El correo electrónico no es válido");
          document.getElementById("errorMsg").innerHTML = "El correo electrónico no es válido";
          document.getElementById("errorMsg").style.display = 'block';
          return;
        }
        fetch(`${baseUrl}/signup`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            correo: user,
            password: pass
          })
        })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          if (data.code === 200) {
            // Guarda el token en el local storage
            // Guardar valores en local storage
            // localStorage.setItem('correo', data['correo']);
            // localStorage.setItem('id_alumno', data['id_alumno']);
            document.cookie = `correo=${data.data.correo}`;
            document.cookie = `id_alumno=${data.data['id_alumno']}`;
            // Usa pushState() para agregar la URL actual al historial del navegador
            window.history.pushState({}, null, `${window.location.href}`);
            // Usa replace() para cambiar a la página de menú
            window.location.replace(`${baseUrl}/menu`);
          }
           else {
            document.getElementById('errorInicioSesion').innerHTML = data.message;
            document.getElementById('errorInicioSesion').style.display = 'block';
          }
        })
        .catch(error => console.error(error));
        

}

function validarCorreoElectronico(correo) {
  // Expresión regular para validar el formato de un correo electrónico
  const expresionRegular = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Verificar si el correo cumple con el formato
  return expresionRegular.test(correo);
}
