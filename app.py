from flask import Flask, request, jsonify, render_template
import psycopg2
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
DB_HOST = "localhost"
DB_NAME = "alumnos_db"
DB_USER = "postgres"  # Usuario por defecto de PostgreSQL
DB_PASS = "abc123"

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/guardar_alumno', methods=['POST'])
def guardar_alumno():
    try:
        # Obtener datos del formulario
        matricula = request.form['matricula']
        nombre = request.form['nombre']
        edad = request.form['edad']

        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()

        # Ejecutar la consulta
        sql = "INSERT INTO alumnos (matricula, nombre, edad) VALUES (%s, %s, %s)"
        cur.execute(sql, (matricula, nombre, edad))
        conn.commit()
        
        # Cerrar la conexión
        cur.close()
        conn.close()

        return jsonify({'message': 'Alumno guardado correctamente'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
