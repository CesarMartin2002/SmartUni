
window.onload = function() {
    alert("base url:");
  };

  function imprimirArgumento(arg) {
    console.log(arg);
  }



function registrarse(user, pass, rpass) {

console.log("Usuario " + user + " y contraseña " + pass + " y repite contraseña " + rpass);
        //call a java servlet (url GetInicioSesion) that logs in with user.value and pass.value
        if (pass != rpass) {    
            console.log("Las contraseñas no coinciden");
        document.getElementById("errorMsg0").style.display = 'block';

            return;
        }
        
        console.log("justo antes del fetch");
        let url = "GetInicioSesion?correo=" + user + "&contrasenna=" + pass;
        console.log("La url es: "+ url)
        fetch(url)
       
        .then(response => response.json())
      .then(data => {
        //handle data
       console.log("entro en el then data");

        console.log(data.islogged);
        if (data.islogged == true) {
            console.log("redirijo a la pagina de bienvenida");
            window.location.replace("bienvenida.html");
      }else{
        document.getElementById("errorInicioSesion").style.display = 'block';
        
      }


      })
      .catch(error => {
       console.log("entro en el then error");
        document.getElementById("errorInicioSesion").style.display = 'block';


        //handle error
      });

        /*
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (data == "true") {
                        console.log("Usuario " + user.value + " y contraseña " + pass.value);
                        window.location.href = "index.html";
                    } else {
                        alert("Usuario o contraseña incorrectos");
                    }
                })
                .catch(error => console.log(error));
            */
 
        


/*
        {
        data:  {"correo" : user, "contrasenna":pass},
                url:   "GetInicioSesion",
                error: function(jqXHR, textStatus, errorThrown)
                {
                },
                type:  'post',
                async: false,
                success:  function (response)
                {
                    console.log(response);
                }
        
}
*/
}



