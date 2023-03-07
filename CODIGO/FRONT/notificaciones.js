window.onload= function(){
  let x = document.cookie;
  if(!x.includes("correo")){
      alert("Debes iniciar sesión para acceder a esta página.");
      window.location.replace("/Securer");
  }
  getNotif(getCookie("correo"));
}

function llamadaAPI(url){
fetch(url)
.then(response => response.json())
.then(data => {
//handle data
console.log(data);
})
.catch(error => {
//handle error
});

}

function getNotif(user) {

  console.log("Usuario " + user );
          //call a java servlet (url GetInicioSesion) that logs in with user.value and pass.value
          console.log("justo antes del fetch");
          let url = "GetNotificacion?correo=" + user;
          console.log("La url es: "+ url)
          fetch(url)
         
          .then(response => response.json())

        .then(data => {
          //handle data
         console.log("entro en el then data");
         console.log(data);
         console.log(data.length);

         for (var i=0; i < data.length; i++) {
          console.log(data[i])
         console.log("añado la " + i);

          addElement(data[i].descripcion,"Ayer");
       }
  
  
        })
        .catch(error => {
         console.log("entro en el then error");
          document.getElementById("errorInicioSesion").style.display = 'block';
  
  
          //handle error
        });
  
  
  }

  function addElement(descripcion,fecha) {
    console.log(descripcion);
    document.getElementById('menu').innerHTML = document.getElementById('menu').innerHTML+('<a href="#" class="btn"><div><span>'+descripcion+'</span><p>'+fecha+'</p></div><img class="icon" src="https://cdn-icons-png.flaticon.com/512/1843/1843344.png" alt="papelera"></a>');
    /*
    console.log("añado la notificacion");
    console.log("Creo las cosas");

    // create a new div element
    const newA = document.createElement("a");
    newA.classList.add("btn");
    const newDiv = document.createElement("div");
    const newSpan = document.createElement("span");
    const newP = document.createElement("p");
    const newImg = document.createElement("img");
    newImg.classList.add("icon");

  
    console.log("doy contenido");
  
    // and give it some content
    const newContentSpan = document.createTextNode(descripcion);
    const newContentP = document.createTextNode(fecha);
  
    console.log("añado hijos");

    // add the text node to the newly created div
    
    newSpan.innerText  = (newContentSpan);
    newP.innerText  =(newContentP);
    newImg.src = "https://cdn-icons-png.flaticon.com/512/1843/1843344.png";
    newDiv.appendChild(newSpan);
    newDiv.appendChild(newP);
    newDiv.appendChild(newImg);
    newA.appendChild(newDiv);
    // add the newly created element and its content into the DOM
    console.log("lo meto dentro de wea");

    const currentDiv = document.getElementById("menu");
    console.log("lo meto dentro de wea2");
    document.body.insertBefore(newA, currentDiv);*/
  }

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  