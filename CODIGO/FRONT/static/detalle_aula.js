window.onload= function(){
    let x = document.cookie;
    if(!x.includes("correo")){
        alert("Debes iniciar sesión para acceder a esta página.");
        window.location.replace("/");

    }
    cargarDatos();
}


async function cargarDatos() {
  // Obtiene los valores de las aulas generando un botón con la información de cada una
  id=parseInt(getLastPathParameter());
  fetch(`/aulas/asignaturas/${id}`)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      console.log(data.length);
      if (data.data && Object.keys(data.data).length > 0) {
        mostrarDatos(data);
    } else {
        var mensaje = 'No se imparten asignaturas en este aula.';
        document.getElementById('aulas').innerHTML = `<h2 style="color:red">${mensaje}</h2>`;
      }
    });
}


function getLastPathParameter() {
    const path = window.location.pathname;
    const pathSegments = path.split("/");
    return pathSegments[pathSegments.length - 1];
  }

// Función que recibe el JSON y muestra las aulas en la página
function mostrarDatos(data) {
  var aula = data.data;
  console.log(aula);
  console.log(aula.length);
  var html = '';

  var nombre_aula = `Aula ${aula[0].nombre}`;

  html += `
      <div class="aula">
      <h1>${nombre_aula}</h1>  
      </div>
      <br>
      `;   
  //consultar las asignaturas de un aula
  var asignaturas = '';
  for (var i = 0; i < aula.length; i++) {
    var descripcion = `Asignatura: ${aula[i].descripcion}`;
    var dia = `Fecha: ${aula[i].dia}`;
    var hora_inicio = `Desde: ${aula[i].hora_inicio}`;
    var hora_fin = `Hasta: ${aula[i].hora_fin}`;
    
    //asignaturas += `${descripcion}<br>${dia}<br>${hora_inicio}<br><br>`;
    
    html += `
      <div class="aula">
        <h2>${descripcion}</h2>
        <h2>${dia}</h2>
        <h2>${hora_inicio}</h2>
        <h2>${hora_fin}</h2>
      </div>
      <br>
    `;

  }
  document.getElementById('aulas').innerHTML = html;
}
