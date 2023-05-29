
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

/*taquillas.innerHTML=`
    <h1>Lista de taquillas</h1>
    <h2>Selecciona la taquilla que deseas ver en detalle</h2>
`;*/

/*fetch('/BACK/endpoints/taquillas.py/taquillas')*/ 

fetch('/BACK/endpoints/taquillas/taquillas')
  .then(response => response.json())
  /*por defecto ya esta HACIENDO una llamada GET, si es una llamada PUT sw pone 'Method: put'*/
  .then(data => {
    // Actualizar el contenido de taquillas con los datos obtenidos
    taquillas.innerHTML = `
        <h1>Lista de taquillas</h1>
        <h2>Selecciona la taquilla que deseas ver en detalle</h2>
        <table>
            <thead>
                <tr>
                    <th>Id_taquilla</th>
                    <th>Password</th>
                    <th>Ala</th>
                    <th>Piso</th>
                    <th>Pasillo</th>
                    <th>Ocupado</th>
                    <th>Id_alumno</th>
                </tr>
            </thead>
            <tbody>
                ${data.map(taquilla => `
                    <tr>
                        <td>${taquilla.id_taquilla}</td>
                        <td>${taquilla.password}</td>
                        <td>${taquilla.ala}</td>
                        <td>${taquilla.piso}</td>
                        <td>${taquilla.pasillo}</td>
                        <td>${taquilla.ocupado}</td>
                        <td>${taquilla.id_alumno_alumno}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
  });

