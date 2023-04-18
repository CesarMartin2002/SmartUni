// Define a global variable baseUrl that contains the beginning of the URL
let baseUrl = window.location.protocol + "//" + window.location.host;

// Make a method to log in
function iniciarSesion(user, pass) {
  console.log("Usuario " + user + " y contraseña " + pass);

  // Call a Java servlet (url GetInicioSesion) that logs in with user.value and pass.value
  console.log("justo antes del fetch");
  fetch(baseUrl+"/login", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      correo: 'user',
      password: 'pass'
    })
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
  


  // let url = baseUrl + "/GetInicioSesion?correo=" + user + "&contrasenna=" + pass;
  // console.log("La url es: " + url);
  // fetch(url)
  //   .then(response => response.json())
  //   .then(data => {
  //     console.log("entro en el then data");
  //     console.log(data.islogged);
  //     if (data.islogged == true) {
  //       console.log("redirijo a la pagina de bienvenida");
  //       window.location.replace("bienvenida.html");
  //     } else {
  //       document.getElementById("errorInicioSesion").style.display = "block";
  //     }
  //   })
  //   .catch(error => {
  //     console.log("entro en el then error");
  //     document.getElementById("errorInicioSesion").style.display = "block";
  //     // Handle error
  //   });
}

window.onload = function() {
  console.log("base url: " + baseUrl);
};