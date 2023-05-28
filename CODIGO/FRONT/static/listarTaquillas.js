
//cookie de inicio sesion
window.onload= function(){
  let x = document.cookie;
  if(!x.includes("correo")){
      alert("Debes iniciar sesión para acceder a esta página.");
      window.location.replace("/");

  }
}
const btnMenu = Array.from(document.querySelectorAll('.btn-menu'));

var taquillas = document.getElementById("taquillas");
taquillas.innerHTML
