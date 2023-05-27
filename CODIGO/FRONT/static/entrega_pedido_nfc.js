const baseUrl = `${window.location.protocol}//${window.location.host}`;

window.onload = function () {
  let x = document.cookie;
  if (!x.includes("correo")) {
    alert("Debes iniciar sesión para acceder a esta página.");
    window.location.replace("/");
  }
};

const btnScan = document.getElementById("scan-btn");

btnScan.addEventListener("click", async () => {
  const header = document.getElementById("header-info");
  header.innerHTML = "Aproxime un NFC";

  const serialNumber = "04:b2:36:58:70:00:00"; // Aquí puedes reemplazar con el serial que desees para hacer pruebas

  try {
    await handleNFCRead(serialNumber);

    const idAlumno = getCookieValue("id_alumno");
    const idPedido = getLastPathParameter();

    const data = {
      num_serie: serialNumber,
      id_alumno: idAlumno,
      estado: 3,
    };

    const response = (await sendPutRequest(idPedido, data)).json();

    if (response.status === 200) {
      header.innerHTML = "Éxito";
    } else {
      header.innerHTML = response.data.message || "Error";
    }
  } catch (error) {
    console.error("Error:", error);
    header.innerHTML = "Error: " + error.message;
  }
});

async function handleNFCRead(serialNumber) {
  const header = document.getElementById("header-info");
  header.innerHTML = "Serial del NFC: " + serialNumber;
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

