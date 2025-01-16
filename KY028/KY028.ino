#include <DHT.h>

// Definimos los pines de conexión para los sensores
const int ky028_AO = A0;  // Pin analógico del KY-028
const int ky028_DO = 22;  // Pin digital del KY-028 (opcional)

const int ard364_AO = A1; // Pin analógico del Ard-364
const int ard364_DO = 23; // Pin digital del Ard-364 (opcional)

const int ky015_pin = 24; // Pin de señal del KY-015

// Tipo de sensor KY-015 (usa DHT11 o DHT22, según corresponda)
#define DHTTYPE DHT11
DHT dht(ky015_pin, DHTTYPE);

void setup() {
  // Iniciamos la comunicación serial
  Serial.begin(115200);
  Serial.println("Iniciando lectura de sensores...");

  // Inicializamos el sensor KY-015
  dht.begin();
}

void loop() {
  // Leemos el valor analógico del KY-028
  int ky028_sensorValue = analogRead(ky028_AO);
  float ky028_temperature = 64 - 0.175529 * ky028_sensorValue;
  
  // Leemos el valor analógico del Ard-364
  int ard364_sensorValue = analogRead(ard364_AO);
  float ard364_temperature = ard364_sensorValue * (5.0 / 1023.0) * 100.0;
  float air_pressure_pa = map(ky028_temperature, 50, 10, 60081, 103692);

  // Leemos temperatura y humedad del KY-015
  float ky015_temperature = dht.readTemperature();
  float ky015_humidity = dht.readHumidity()-15-(.5*ky028_temperature);
  
  int risk = map(ard364_sensorValue, 0, 1000, 6, 0);
  int fire_alert = -1;  

  if (risk < 3) {
    fire_alert = 0;  
  } else if (risk == 3) {
    fire_alert = 1;  
  } else {
    fire_alert = 2; 
  }


  // Verificamos si la lectura del KY-015 es válida
  if (isnan(ky015_temperature) || isnan(ky015_humidity)) {
    Serial.println("{\"error\":\"Error al leer el KY-015\"}");
  } else {
    // Imprimimos los datos en formato JSON
    Serial.print("{\"air_pressure_pa\":");
    Serial.print(air_pressure_pa);
    Serial.print(", \"fire_alert_status\":");
    Serial.print(fire_alert);
    Serial.print(", \"temperature_c\":");
    Serial.print(ky028_temperature, 2);
    Serial.print(", \"humidity_percent\":");
    Serial.print(ky015_humidity, 2);
    Serial.println("}");
  }

  // Pausa antes de la siguiente lectura
  delay(1200);
}
