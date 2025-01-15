#include <UbidotsESPMicro.h>

// Define tu token de Ubidots
const char* TOKEN = "tu_api_token"; // Reemplaza con tu API token de Ubidots

// Pines del sensor
const int pinAO = A0; // Pin analógico para leer la temperatura
const int pinDO = 22; // Pin digital, si necesitas leer una salida digital

// Crea el cliente Ubidots
Ubidots client(TOKEN);

void setup() {
  // Iniciamos la comunicación serial
  Serial.begin(9600);

  // Inicializa la conexión serial hacia el puerto de Ubidots
  Serial.println("Iniciando conexión con Ubidots...");
}

void loop() {
  // Lee el valor analógico del sensor
  int sensorValue = analogRead(pinAO);

  // Calcula la temperatura con la fórmula del sensor KY-028
  float temperature = 65.315 - 0.175529 * sensorValue;

  // Envía los datos a Ubidots
  client.add("temperature", temperature); // Agrega la variable de temperatura
  bool result = client.sendAll();         // Envía los datos

  // Imprime información en el monitor serial
  Serial.print("Sensor Raw Value: ");
  Serial.print(sensorValue);
  Serial.print("\nTemperatura: ");
  Serial.print(temperature);
  Serial.println(" °C");

  // Verifica si los datos se enviaron correctamente
  if (result) {
    Serial.println("Datos enviados a Ubidots correctamente.");
  } else {
    Serial.println("Error al enviar datos a Ubidots.");
  }

  // Espera 1.2 segundos antes de la siguiente lectura
  delay(1200);
}
