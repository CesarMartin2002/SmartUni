/* 
window.onload= function(){
    let x = document.cookie;
    if(!x.includes("correo")){
        alert("Debes iniciar sesión para acceder a esta página.");
        window.location.replace("/");

    }
}
const btnMenu = Array.from(document.querySelectorAll('.btn-menu'));
**/
var pass = 1234;
var datos = document.getElementById("datos");

datos.innerHTML=`
    <h1>Reserva de taquilla</h1>
    <h2>¿Seguro que deseas reservar esta taquilla?</h2>
`;

