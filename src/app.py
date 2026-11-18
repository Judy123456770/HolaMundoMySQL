
from flask import Flask
import mysql.connector
import os
import time

app = Flask(__name__)

def conectar_bd():
    for intento in range(30):
        try:
            conexion = mysql.connector.connect(
                host=os.getenv("DB_HOST", "db"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "123456"),
                database=os.getenv("DB_NAME", "holamundo")
            )
            return conexion
        except mysql.connector.Error:
            time.sleep(2)

    raise Exception("No se pudo conectar a MySQL")

@app.route("/")
def inicio():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("SELECT 'Conexión exitosa con MySQL' ")
        resultado = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        return f"""
        <h1>¡Hola Mundo!</h1>
        <h2>Aplicación web con Python y Flask</h2>
        <p>Base de datos: MySQL</p>
        <p>{resultado}</p>
        """

    except Exception as error:
        return f"Error de conexión: {error}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

