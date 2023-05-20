
window.onload= function(){
    let x = document.cookie;
    if(!x.includes("correo")){
        alert("Debes iniciar sesión para acceder a esta página.");
        window.location.replace("/");

    }
}
const btnMenu = Array.from(document.querySelectorAll('.btn-menu'));

btnMenu.forEach((btns) => {
    btns.addEventListener('click', () => {
        btnMenu.forEach((btns) => {
            btns.classList.remove('selected');
        });
        btns.classList.add('selected');
    });
});