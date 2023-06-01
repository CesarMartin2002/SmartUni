const baseUrl = `${window.location.protocol}//${window.location.host}`;

window.onload = function () {
  let x = document.cookie;
  if (!x.includes("correo")) {
    alert("Debes iniciar sesión para acceder a esta página.");
    window.location.replace("/");
  }
};

const btnScan = document.getElementById("scan-btn");
const btnSimulateScan = document.getElementById("simulate-scan-btn");

btnScan.addEventListener("click", escaneoReal);
btnSimulateScan.addEventListener("click", escaneoSimulado);

async function scanNFC() {
  try {
    return new Promise((resolve, reject) => {
      const ndef = new NDEFReader();
      ndef.onreading = event => {
        const serialNumber = event.serialNumber;
        console.log(`> Serial Number: ${serialNumber}`);
        resolve(serialNumber);
      };
      ndef.onreadingerror = () => {
        console.error("No se puede leer la tarjeta NFC. ¿Intentar con otra?");
        document.getElementById("header-info").innerHTML = "No se puede leer la tarjeta NFC. ¿Intentar con otra?";
        reject(null);
      };
      ndef.scan();
    });
  } catch (error) {
    console.error("Error al iniciar el escaneo NFC:", error);
    document.getElementById("header-info").innerHTML = "Error al iniciar el escaneo NFC: " + error.message;
    return null;
  }
}


async function escaneoReal(){
  var ncf = await scanNFC();
  console.log(ncf);
  if (ncf != null){
    ncf = ncf.toString();
    // document.getElementById("header-info").innerHTML = ncf;
    consultarPedidoNfc(ncf);

  }
}

function escaneoSimulado(){
  const ncf = "123456789";
  // document.getElementById("header-info").innerHTML = ncf;
  consultarPedidoNfc(ncf);
}

function consultarPedidoNfc(nfc) {
  //el id del pedido se obtiene de la url de la pagina pasandolo a int
  const idPedido = parseInt(getLastPathParameter());
  const id_alumno = parseInt(getCookieValue("id_alumno"));
  const url = `${baseUrl}/cafeteria/pedidos/nfc/${idPedido}`;
  const data = {
    num_serie: nfc,
    id_alumno: id_alumno,
    estado: 3
  };

  fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => {
      if (response.ok) {
        document.getElementById("header-info").innerHTML = "Verificación exitosa.";
        //cambiamos en el css el color de la variable en root llamada --main-bg a #58e76b
        document.documentElement.style.setProperty('--main-bg', '#58e76b');
        //ocultamos el boton de escanear
        document.getElementById("scan-btn").style.display = "none";
        //ocultamos el boton de simular escaneo
        document.getElementById("simulate-scan-btn").style.display = "none";
      } else {
        document.getElementById("header-info").innerHTML = "Verificación fallida.";
        //cambiamos en el css el color de la variable en root llamada --main-bg a #e75858
        document.documentElement.style.setProperty('--main-bg', '#e75858');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}



function getCookieValue(name) {
  const cookies = document.cookie.split(";").map((cookie) => cookie.trim());
  for (const cookie of cookies) {
    if (cookie.startsWith(name + "=")) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

function getLastPathParameter() {
  const path = window.location.pathname;
  const pathSegments = path.split("/");
  return pathSegments[pathSegments.length - 1];
}

async function sendPutRequest(idPedido, data) {
  const url = `${baseUrl}/cafeteria/pedidos/nfc/${idPedido}`;

  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    return response;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}
