// Define una variable global baseUrl que contiene el inicio de la URL
const baseUrl = `${window.location.protocol}//${window.location.host}`;
var filtro = "";
function cargarDatos(){
  //obtiene los valores de los records generando un boton con la informacion de cada uno
  filtro = document.getElementById("input").value;
  if (filtro == undefined) filtro = "";
  ruta= `${baseUrl}/cafeteria/productos?filtro=${filtro}`;
  console.log(ruta);
  fetch(ruta)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      mostrarDatos(data);
      
    }
    )
}
//llamamos a cargarDatos al cargar la pagina
window.onload = cargarDatos();

//funcion que recibe el json y lo muestra en la pagina
function mostrarDatos(data){
  var productos = data.data;
  var html = '';
  for (var i = 0; i < productos.length; i++) {
    nombre = productos[i].descripcion;
    precio = productos[i].precio;
    html += `<button class="btn btn-primary" onclick="window.location.href = 'productos/${productos[i].id_producto}'">${nombre}  |  ${precio}</button><br>`;
  }
  document.getElementById('productos').innerHTML = html;
}
