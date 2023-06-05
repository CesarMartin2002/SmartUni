const id_producto = getCookie('id_producto');

function getLastPathParameter() {
    const path = window.location.pathname;
    const pathSegments = path.split("/");
    return pathSegments[pathSegments.length - 1];
  }

async function cargarDatos() {
    // Obtiene los valores de los productos sacando la información de cada uno
    id = parseInt(getLastPathParameter()); 
    console.log(id)
    fetch(`/cafeteria/productos/${id}`)
      .then(response => response.json())
      .then(data => {
        console.log("Esto es data"+data);
        console.log(data);
        if (data.data && Object.keys(data.data).length > 0) {
            console.log("se mete");
            mostrarDatos(data);
        } else {
            var mensaje = 'No existe este producto.';
            document.getElementById('producto').innerHTML = `<p>${mensaje}</p>`;
        }
        })
        .catch(error => {
        console.error(error);
        });
  }
  
  window.onload = cargarDatos();

  function mostrarDatos(data) {
    var producto = data.data;
    console.log(producto);
    var html = '';
    var nombre = `${producto.descripcion}`;
    var precio = `Precio: ${producto.precio}`;
    var detalles = `Descripcion: ${producto.detalles}`;
    var imagen = ` ${producto.imagen}`;
    
    html += `
        <div class="detalle_producto">
        <h2>${nombre}</h2>
        <h3>${precio}</h3>  
        <h3>${detalles}</h3> 
        <img src="${imagen}" alt="imagen del producto">
        
        </div>
      <br>
    `;
    
    document.getElementById('producto').innerHTML = html;
  }

// Función para obtener el valor de una cookie por su nombre
function getCookie(name) {
    var cookieName = name + '=';
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookieArray = decodedCookie.split(';');
  
    for (var i = 0; i < cookieArray.length; i++) {
      var cookie = cookieArray[i];
      while (cookie.charAt(0) === ' ') {
        cookie = cookie.substring(1);
      }
      if (cookie.indexOf(cookieName) === 0) {
        return cookie.substring(cookieName.length, cookie.length);
      }
    }
  
    return '';
  }