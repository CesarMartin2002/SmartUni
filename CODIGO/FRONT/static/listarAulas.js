// Define una variable global baseUrl que contiene el inicio de la URL
const baseUrl = `${window.location.protocol}//${window.location.host}`;

function cargarDatos() {
  // Obtiene los valores de las aulas generando un botón con la información de cada una
  fetch(`${baseUrl}/aulas`)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      mostrarDatos(data);
    });
}

// Llamamos a cargarDatos al cargar la página
window.onload = cargarDatos();

// Función que recibe el JSON y muestra las aulas en la página
function mostrarDatos(data) {
  var aulas = data.data;
  var html = '';

  for (var i = 0; i < aulas.length; i++) {
    var nombre_aula = `Aula ${aulas[i].nombre}`;

    html += `
      <div class="aula">
        <button class="btn btn-primary" onclick="window.location.href = '/detalleAula/${aulas[i].id_aula}'">
          ${nombre_aula}
        </button>
      </div>
      <br>
    `;
  }
  document.getElementById('aulas').innerHTML = html;
}
