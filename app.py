from flask import Flask, render_template, jsonify
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import struct
import mysql.connector
import datetime
import socket
import flask


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("temperatura.html")

@app.route("/temperature")
def temperature():
    cnx = mysql.connector.connect(user='cris', password='12345',
                              host='34.176.16.130',
                              database='cris_temperatura')
    cursor = cnx.cursor()
    cursor.execute('SELECT temperature FROM temperature ORDER BY id DESC LIMIT 1')
    temperature = cursor.fetchone()

    if temperature is None:
        # Si no hay ningún valor registrado, asignamos el último valor registrado a temperature
        cursor.execute('SELECT temperature FROM temperature ORDER BY id DESC LIMIT 1 OFFSET 1')
        temperature = cursor.fetchone()[0]

    else:
        temperature = temperature[0]

    print('Obteniendo la temperatura actual...')
    temperature_formatted = temperature
    return jsonify(temperature=temperature_formatted)


@app.route("/temperature_average")
def temperature_average():
    # Obtener la temperatura media de los últimos 5 minutos
    five_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=5) # 5 minutos atrás
    #temperatures = Temperature.query.filter(Temperature.timestamp >= five_minutes_ago).all() # Temperaturas de los últimos 5 minutos
    #average_temperature = sum(t.temperature for t in temperatures) / len(temperatures) # Temperatura media de los últimos 5 minutos
    #average_temperature_formatted = "{:.2f} °C".format(average_temperature) # Temperatura media de los últimos 5 minutos formateada
    #return jsonify(average_temperature=average_temperature_formatted) # Devolver la temperatura media de los últimos 5 minutos formateada
    return jsonify(average_temperature="0.00 °C")
    
if __name__ == "__main__":
    app.run(debug=True)
