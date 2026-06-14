from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
import psycopg2
import psycopg2.extras
import pandas as pd
import io
from config import Config

reportes_bp = Blueprint('reportes', __name__)

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

@reportes_bp.route('/reportes')
def panel_reportes():
    # Seguridad: Admin (1), Gerente (2), Supervisor (3), Analista (6)
    if 'id_usuario' not in session or session.get('id_rol') not in [1, 2, 3, 6]:
        flash('Acceso denegado. Módulo exclusivo para jefaturas.', 'danger')
        return redirect(url_for('auth.dashboard'))
    return render_template('reportes.html')

@reportes_bp.route('/reportes/descargar_fallas')
def descargar_fallas():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # CORREGIDO: Uso de comillas dobles para alias con espacios en Postgres
        query = """
            SELECT ot.id_ot as "Nro OT", e.codigo_patrimonial as "Equipo", e.nombre as "Descripcion",
                   ot.tipo_mantenimiento as "Tipo Mantenimiento", ot.fecha_creacion as "Fecha Reporte", 
                   ot.fecha_cierre as "Fecha Cierre", ot.diagnostico as "Diagnostico Tecnico"
            FROM ordenes_trabajo ot
            INNER JOIN equipos e ON ot.id_equipo = e.id_equipo
            WHERE ot.estado = 'Cerrada'
            ORDER BY ot.fecha_cierre DESC
        """
        cursor.execute(query)
        datos = cursor.fetchall()
    except Exception as e:
        print(f"Error en BD: {e}")
        datos = []
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()

    # Si hay datos los pasamos a Pandas, si no, creamos un Excel con los títulos vacíos
    if datos:
        df = pd.DataFrame(datos)
    else:
        df = pd.DataFrame(columns=['Nro OT', 'Equipo', 'Descripcion', 'Tipo Mantenimiento', 'Fecha Reporte', 'Fecha Cierre', 'Diagnostico Tecnico'])

    # Generar el Excel en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Historial de Fallas')
    output.seek(0)

    return send_file(output, download_name="Reporte_Fallas_ALO.xlsx", as_attachment=True)

@reportes_bp.route('/reportes/descargar_eficiencia')
def descargar_eficiencia():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # CORREGIDO: Comillas dobles para alias en Postgres
        query = """
            SELECT version_modelo as "Version IA", fecha_entrenamiento as "Fecha de Actualizacion", 
                   (precision_score * 100) as "Precision (%)", (recall_score * 100) as "Sensibilidad (%)", 
                   (f1_score * 100) as "F1-Score (%)", parametros as "Parametros Tecnicos"
            FROM metricas_modelo_ml
            ORDER BY id_metrica DESC
        """
        cursor.execute(query)
        datos = cursor.fetchall()
    except Exception as e:
        print(f"Error en BD: {e}")
        datos = []
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()

    if datos:
        df = pd.DataFrame(datos)
    else:
        df = pd.DataFrame(columns=['Version IA', 'Fecha de Actualizacion', 'Precision (%)', 'Sensibilidad (%)', 'F1-Score (%)', 'Parametros Tecnicos'])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Eficiencia ML')
    output.seek(0)

    return send_file(output, download_name="Reporte_Eficiencia_ML.xlsx", as_attachment=True)

@reportes_bp.route('/reportes/imprimir_fallas')
def imprimir_fallas():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        query = """
            SELECT ot.id_ot, e.codigo_patrimonial as equipo, e.nombre as descripcion,
                   ot.tipo_mantenimiento, ot.fecha_creacion, ot.fecha_cierre, ot.diagnostico
            FROM ordenes_trabajo ot
            INNER JOIN equipos e ON ot.id_equipo = e.id_equipo
            WHERE ot.estado = 'Cerrada'
            ORDER BY ot.fecha_cierre DESC
        """
        cursor.execute(query)
        datos = cursor.fetchall()
    except Exception as e:
        datos = []
        flash(f"Error al generar reporte: {e}", "danger")
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()
    
    from datetime import datetime
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    columnas = ['Nro OT', 'Código', 'Descripción', 'Tipo', 'Fecha Reporte', 'Fecha Cierre', 'Diagnóstico Técnico']
    return render_template('reporte_print.html', titulo="Historial de Fallas y Mantenimientos", 
                           datos=datos, columnas=columnas, tipo='fallas', fecha=fecha_actual)

@reportes_bp.route('/reportes/imprimir_eficiencia')
def imprimir_eficiencia():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # CORREGIDO: Se cambiaron los backticks (`) por comillas dobles (") para la palabra reservada 'precision'
        query = """
            SELECT version_modelo, fecha_entrenamiento, 
                   ROUND(precision_score * 100, 2) as "precision", 
                   ROUND(recall_score * 100, 2) as recall, 
                   ROUND(f1_score * 100, 2) as f1, parametros
            FROM metricas_modelo_ml
            ORDER BY id_metrica DESC
        """
        cursor.execute(query)
        datos = cursor.fetchall()
    except Exception as e:
        datos = []
        flash(f"Error al generar reporte: {e}", "danger")
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()
    
    from datetime import datetime
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    columnas = ['Versión del Modelo IA', 'Fecha de Actualización', 'Precisión', 'Sensibilidad', 'F1-Score', 'Parámetros Utilizados']
    return render_template('reporte_print.html', titulo="Reporte de Eficiencia (Machine Learning)", 
                           datos=datos, columnas=columnas, tipo='eficiencia', fecha=fecha_actual)