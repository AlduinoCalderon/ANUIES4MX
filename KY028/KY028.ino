// Definimos los pines de conexión
const int pinAO = A0; // Pin analógico para leer la temperatura
const int pinDO = 22; // Pin digital, opcional

void setup() {
  // Iniciamos la comunicación serial
  Serial.begin(9600);
  Serial.println("Iniciando lectura de temperatura...");
}

void loop() {
  // Leemos el valor analógico del sensor
  int sensorValue = analogRead(pinAO);

  // Convertimos el valor analógico a temperatura (según la fórmula del KY-028)
  float temperature = 64 - 0.175529 * sensorValue;

  // Imprimimos los datos en formato JSON para facilitar el procesamiento externo
  Serial.print("{\"temperature\":");
  Serial.print(temperature, 2); // Dos decimales para la temperatura
  Serial.println("}");

  // Pausa antes de la siguiente lectura
  delay(1200);
}
