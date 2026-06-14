from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2.extras
from config import Config
import random

analista_bp = Blueprint('analista', __name__)

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

@analista_bp.route('/analista', methods=['GET', 'POST'])
def laboratorio_ml():
    # Seguridad: Solo Administrador (1) y Analista (6)
    if 'id_usuario' not in session or session.get('id_rol') not in [1, 6]:
        flash('Acceso denegado. Módulo exclusivo para Analistas de Datos.', 'danger')
        return redirect(url_for('auth.dashboard'))

    # Lógica para Reentrenar el Modelo (CU-22)
    if request.method == 'POST':
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Simulamos que el modelo lee los nuevos datos y mejora ligeramente su precisión
        nueva_precision = random.uniform(0.92, 0.96)
        nuevo_recall = random.uniform(0.90, 0.95)
        nuevo_f1 = (2 * nueva_precision * nuevo_recall) / (nueva_precision + nuevo_recall)
        
        try:
            # Obtenemos la última versión para sumarle 1
            cursor.execute("SELECT COUNT(*) as total FROM metricas_modelo_ml")
            total_versiones = cursor.fetchone()['total'] + 1
            nueva_version = f"v{total_versiones}.0 (Random Forest Optimizado)"

            sql = """INSERT INTO metricas_modelo_ml (precision_score, recall_score, f1_score, version_modelo, parametros) 
                     VALUES (%s, %s, %s, %s, 'n_estimators=150, auto_balance=True')"""
            cursor.execute(sql, (nueva_precision, nuevo_recall, nuevo_f1, nueva_version))
            conexion.commit()
            flash(f'¡Modelo reentrenado con éxito! Nueva versión {nueva_version} generada.', 'success')
        except Exception as e:
            conexion.rollback() # VITAL: Evita que Postgres congele el hilo de transacciones
            flash(f'Error durante el entrenamiento: {str(e)}', 'danger')
        finally:
            conexion.close()
            
        # Patrón PRG: Redirigimos para limpiar la petición POST y evitar que un F5 reentrene de nuevo
        return redirect(url_for('analista.laboratorio_ml'))

    # --- LÓGICA PARA EL MÉTODO GET (Mostrar la vista) ---
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Obtener el historial de entrenamientos (CU-23)
        cursor.execute("SELECT * FROM metricas_modelo_ml ORDER BY id_metrica DESC")
        historial = cursor.fetchall()
        
        # La métrica más reciente para las tarjetas principales
        metrica_actual = historial[0] if historial else None
    except Exception as e:
        historial = []
        metrica_actual = None
        flash(f'Error al cargar el historial de métricas: {str(e)}', 'danger')
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()

    return render_template('analista.html', historial=historial, actual=metrica_actual)