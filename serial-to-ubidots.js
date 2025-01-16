
const Readline = require("@serialport/parser-readline");
const axios = require("axios");
const serialport = require("serialport");

// Create a port
const port = new serialport({
  path: '/dev/cu.usbmodem21301',
  baudRate: 9600,
}); 

const parser = port.pipe(new Readline({ delimiter: "\n" }));

// URL de Ubidots
const UBIDOTS_URL = "http://industrial.api.ubidots.com/api/v1.6/devices/device1/";
const TOKEN = "BBUS-Y9tERuNnMUXEJJW6Z9fGz0ZQHx8LTs";

// Manejo de datos recibidos desde el puerto serial
parser.on("data", (data) => {
  try {
    // Aquí asumimos que el dato recibido es un JSON válido desde el Arduino
    const jsonData = JSON.parse(data);
    
    // Enviamos el JSON a Ubidots mediante un POST
    axios
      .post(UBIDOTS_URL, jsonData, {
        headers: {
          "X-Auth-Token": TOKEN,
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        console.log("Enviado a Ubidots:", jsonData);
        console.log("Código de respuesta:", response.status);
      })
      .catch((error) => {
        console.error("Error al enviar a Ubidots:", error.response ? error.response.data : error.message);
      });

  } catch (err) {
    console.error("Error procesando los datos del puerto serial:", err);
  }
});

// Manejo de errores del puerto serial
port.on('error', (err) => {
  console.error("Error en el puerto serial:", err.message);
});
