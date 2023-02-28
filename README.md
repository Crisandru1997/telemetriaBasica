from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import struct
import datetime
import pymysql

# Variables
IP_ADDRESS = "192.168.0.100"
PORT = 502
ADDRESS = 136 # Corriente (media)
listado_final = list() # Listado para invertir los datos.

# Conexión con el tablero.
client = ModbusTcpClient(IP_ADDRESS, PORT)
client.connect()
if client.connect():
    print("Conectado con éxito al dispositivo Modbus")
else:
    print("Error de conexión con el dispositivo Modbus")

# Conexión con la base de datos.
conn = pymysql.connect(
    host="34.176.16.130",
    user="cris",
    password="12345",
    db="cris_temperatura",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conn.cursor() as cursor:
        while True:
            if client.connect():
                try:
                    result = client.read_holding_registers(ADDRESS, 2, slave=2)
                    l1 = result.registers[0]
                    l2 = result.registers[1]
                    listado_final.append(l2)
                    listado_final.append(l1)
                    raw_data = struct.pack("!2H", *listado_final)
                    temp = struct.unpack('!f', raw_data)[0]
                    final = "{:.5f}".format(temp)
                    timestamp = datetime.datetime.now()
                    # Insertar datos en la base de datos.
                    query = "INSERT INTO corriente (corriente, timestamp) VALUES (%s, %s)"
                    values = (final, timestamp)
                    cursor.execute(query, values)
                    conn.commit()
                    print(f"Inserción exitosa en la base de datos: corriente={final}, timestamp={timestamp}")
                    listado_final = list()
                    time.sleep(1)
                except ModbusIOException as e:
                    print("Error de comunicación con el dispositivo Modbus:", e)
            else:
                print("Error de conexión con el dispositivo Modbus")
                break
finally:
    conn.close()
