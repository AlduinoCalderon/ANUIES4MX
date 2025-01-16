import serial
import requests
import json
import time
import glob

def find_arduino_port():
    # Lista todos los dispositivos de tipo tty
    ports = glob.glob('/dev/tty.*')
    
    # Filtra aquellos que contienen 'usbmodem' en su nombre (puede cambiar según tu caso)
    arduino_ports = [port for port in ports if 'usbmodem' in port]
    
    # Si encontró algún puerto, devuelve el primero
    if arduino_ports:
        return arduino_ports[0]
    else:
        print("No se encontró Arduino conectado.")
        return None
SERIAL_PORT = find_arduino_port()
BAUD_RATE = 9600

UBIDOTS_URL = "http://industrial.api.ubidots.com/api/v1.6/devices/device1/"
TOKEN = "BBUS-Y9tERuNnMUXEJJW6Z9fGz0ZQHx8LTs"

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

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

def main():
    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                
                try:
                    json_data = json.loads(data)
                    print(f"Datos recibidos del Arduino: {json_data}")
                    
                 
                    send_to_ubidots(json_data)
                except json.JSONDecodeError:
                    print(f"Error al procesar los datos: {data}")
        except Exception as e:
            print(f"Error en la lectura del puerto serial: {e}. Intentando reconectar...")
          #  SERIAL_PORT = find_arduino_port()
        
     
        time.sleep(1)

if __name__ == '__main__':
    main()
