import serial
import requests
import json
import time
import glob
import pandas as pd
from tensorflow.keras.models import load_model
from datetime import datetime


def find_arduino_port():
    ports = glob.glob('/dev/tty.*')
    arduino_ports = [port for port in ports if 'usbmodem' in port]
    if arduino_ports:
        return arduino_ports[0]
    else:
        print("No se encontró Arduino conectado.")
        return None


SERIAL_PORT = find_arduino_port()
BAUD_RATE = 115200

UBIDOTS_URL = "http://industrial.api.ubidots.com/api/v1.6/devices/device1/"
TOKEN = "BBUS-Y9tERuNnMUXEJJW6Z9fGz0ZQHx8LTs"

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Cargar el modelo
model_path = './my_trained_model.keras'
model = load_model(model_path)

# DataFrame inicial para almacenar datos crudos
df_rawdata_GA = pd.DataFrame()


def send_to_ubidots(data):
    headers = {
        "X-Auth-Token": TOKEN,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(UBIDOTS_URL, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print(f"Datos enviados a Ubidots: {data}")
        else:
            print(f"Error al enviar datos a Ubidots: {response.status_code}")
    except Exception as e:
        print(f"Error en la conexión con Ubidots: {e}")


def classify_data(df):
    try:
        # Excluir la columna fire_alert_status
        features = df[['air_pressure_pa', 'temperature_c', 'humidity_percent']]
        
        # Realizar predicción
        predictions = model.predict(features)
        
        # Mostrar resultados
        print(f"Predicciones del modelo:\n{predictions}")
    except Exception as e:
        print(f"Error al clasificar los datos: {e}")


def main():
    global df_rawdata_GA
    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                try:
                    json_data = json.loads(data)
                    print(f"Datos recibidos del Arduino: {json_data}")
                    
                    # Agregar los datos al DataFrame
                    df_rawdata_GA = pd.concat([df_rawdata_GA, pd.DataFrame([json_data])], ignore_index=True)
                    
                    # Verificar si se han acumulado 20 registros
                    if len(df_rawdata_GA) >= 20:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        df_name = f"df_{timestamp}"
                        globals()[df_name] = df_rawdata_GA.copy()
                        print(f"Creado DataFrame: {df_name}")
                        
                        # Clasificar los datos
                        classify_data(globals()[df_name])
                        
                        # Limpiar el DataFrame
                        df_rawdata_GA = pd.DataFrame()

                    # Enviar datos a Ubidots
                    send_to_ubidots(json_data)
                except json.JSONDecodeError:
                    print(f"Error al procesar los datos: {data}")
        except Exception as e:
            print(f"Error en la lectura del puerto serial: {e}")
        
        time.sleep(1)


if __name__ == '__main__':
    main()
