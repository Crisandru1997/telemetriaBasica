from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    cnx = mysql.connector.connect(user='cris', password='12345',
                              host='34.176.16.130',
                              database='temperature')
    cursor = cnx.cursor()
    cursor.execute('SELECT temperature FROM temps ORDER BY id DESC LIMIT 1')
    temperature = cursor.fetchone()[0]
    cnx.close()
    return 'La temperatura actual es: {} grados Celsius'.format(temperature)

if __name__ == '__main__':
    app.run(debug=True)
