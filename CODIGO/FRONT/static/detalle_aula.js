window.onload= function(){
    let x = document.cookie;
    if(!x.includes("correo")){
        alert("Debes iniciar sesión para acceder a esta página.");
        window.location.replace("/");

    }
    cargarDatos();
}
const btnMenu = Array.from(document.querySelectorAll('.btn-menu'));
