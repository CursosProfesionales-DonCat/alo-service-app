from flask import Blueprint, render_template, request, flash, session, redirect, url_for
import joblib
import numpy as np
import os
import psycopg2
import psycopg2.extras
from config import Config

predict_bp = Blueprint('predict', __name__)

# CORREGIDO: Conexión nativa a PostgreSQL usando RealDictCursor
def obtener_conexion():
    return psycopg2.connect(
        host=Config.PG_HOST,
        user=Config.PG_USER,
        password=Config.PG_PASSWORD,
        dbname=Config.PG_DB,
        port=Config.PG_PORT,
        cursor_factory=psycopg2.extras.RealDictCursor
    )

@predict_bp.route('/predictivo', methods=['GET', 'POST'])
def modulo_predictivo():
    # Seguridad: Admin, Gerente, Supervisor, Técnico y Analista
    if 'id_usuario' not in session or session.get('id_rol') not in [1, 2, 3, 4, 6]:
        flash('Acceso denegado. Módulo exclusivo para Supervisión y Gerencia.', 'danger')
        return redirect(url_for('auth.dashboard'))

    # 1. Obtener todos los equipos operativos de la BD de forma segura
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_equipo, codigo_patrimonial, nombre, horas_uso FROM equipos WHERE estado != 'Inactivo'")
        equipos = cursor.fetchall()
    except Exception as e:
        equipos = []
        flash(f'Error al conectar con la base de datos de equipos: {str(e)}', 'danger')
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()

    # 2. Cargar el modelo Random Forest (.pkl)
    ruta_modelo = os.path.join(os.getcwd(), 'app', 'ml_core', 'modelo_mantenimiento.pkl')
    try:
        modelo_ml = joblib.load(ruta_modelo)
    except:
        modelo_ml = None

    resultados_ml = []

    # 3. Procesar cada equipo por la Inteligencia Artificial (CU-19 y CU-20)
    if modelo_ml and equipos:
        for eq in equipos:
            horas = eq['horas_uso'] if eq['horas_uso'] else 0
            
            # Simulamos datos de sensores (temperatura y vibración) basados en el desgaste (horas de uso)
            # En un entorno 100% real, esto vendría de sensores IoT de la maquinaria.
            temp_simulada = 75.0 + (horas / 500) 
            vibracion_simulada = 5.0 + (horas / 1000)
            dias_mtto = 120 

            # Predecir con Scikit-Learn
            features = np.array([[horas, temp_simulada, vibracion_simulada, dias_mtto]])
            probabilidades = modelo_ml.predict_proba(features)[0]
            prob_falla = round(probabilidades[1] * 100, 2)

            # Clasificación del Semáforo
            estado = "Bajo Riesgo"
            color = "success"
            if prob_falla >= 75.0:
                estado = "Alto Riesgo (Crítico)"
                color = "danger"
            elif prob_falla >= 40.0:
                estado = "Riesgo Medio (Advertencia)"
                color = "warning"

            resultados_ml.append({
                'id_equipo': eq['id_equipo'],
                'codigo': eq['codigo_patrimonial'],
                'nombre': eq['nombre'],
                'horas': horas,
                'prob_falla': prob_falla,
                'estado': estado,
                'color': color
            })
            
        # Ordenar de mayor a menor riesgo para que el Supervisor vea las urgencias primero
        resultados_ml = sorted(resultados_ml, key=lambda x: x['prob_falla'], reverse=True)

    return render_template('predicciones.html', resultados=resultados_ml, modelo_cargado=(modelo_ml is not None))