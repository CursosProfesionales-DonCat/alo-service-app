from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2.extras
from config import Config

ordenes_bp = Blueprint('ordenes', __name__)

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

@ordenes_bp.route('/ordenes', methods=['GET', 'POST'])
def gestionar_ordenes():
    # Seguridad: Solo usuarios logueados pueden entrar
    if 'id_usuario' not in session:
        return redirect(url_for('auth.login'))

    # Lógica para Registrar una nueva OT (CU-12)
    if request.method == 'POST':
        id_equipo = request.form.get('id_equipo')
        id_tecnico = request.form.get('id_tecnico')
        tipo_mantenimiento = request.form.get('tipo_mantenimiento')
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            sql = """INSERT INTO ordenes_trabajo (id_equipo, id_tecnico, tipo_mantenimiento, estado) 
                     VALUES (%s, %s, %s, 'Pendiente')"""
            cursor.execute(sql, (id_equipo, id_tecnico, tipo_mantenimiento))
            conexion.commit()
            flash('Orden de Trabajo generada y asignada correctamente.', 'success')
        except Exception as e:
            conexion.rollback() # VITAL: Libera la transacción bloqueada en Postgres ante cualquier fallo
            flash(f'Error al generar la OT: {str(e)}', 'danger')
        finally:
            conexion.close()
            
        # Patrón PRG: Redirección inmediata para limpiar el POST y evitar OTs duplicadas con F5
        return redirect(url_for('ordenes.gestionar_ordenes'))

    # --- LÓGICA PARA EL MÉTODO GET (Mostrar la vista y cargar tablas) ---
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Obtener la lista de Equipos (Para el selector)
        cursor.execute("SELECT id_equipo, codigo_patrimonial, nombre FROM equipos WHERE estado != 'Inactivo'")
        lista_equipos = cursor.fetchall()
        
        # Obtener la lista de Técnicos (Buscando el rol 'Técnico' en la BD y que esté activo)
        cursor.execute("""
            SELECT u.id_usuario, u.nombres, u.apellidos 
            FROM usuarios u 
            INNER JOIN roles r ON u.id_rol = r.id_rol 
            WHERE r.nombre = 'Técnico' AND u.estado = TRUE
        """)
        lista_tecnicos = cursor.fetchall()

        # Obtener el historial de Órdenes de Trabajo
        cursor.execute("""
            SELECT ot.id_ot, e.codigo_patrimonial, u.nombres as tecnico, 
                   ot.tipo_mantenimiento, ot.estado, ot.fecha_creacion 
            FROM ordenes_trabajo ot
            INNER JOIN equipos e ON ot.id_equipo = e.id_equipo
            INNER JOIN usuarios u ON ot.id_tecnico = u.id_usuario
            ORDER BY ot.id_ot DESC
        """)
        lista_ordenes = cursor.fetchall()
        
    except Exception as e:
        lista_ordenes = []
        lista_equipos = []
        lista_tecnicos = []
        flash(f'Error al cargar el flujo de órdenes de trabajo: {str(e)}', 'danger')
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()

    return render_template('ordenes.html', ordenes=lista_ordenes, equipos=lista_equipos, tecnicos=lista_tecnicos)