from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2.extras
from config import Config
from datetime import datetime

tecnico_bp = Blueprint('tecnico', __name__)

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

@tecnico_bp.route('/mi_panel', methods=['GET', 'POST'])
def mi_panel():
    # Seguridad: Solo usuarios logueados y con rol Técnico (4) pueden entrar
    if 'id_usuario' not in session or session.get('id_rol') != 4:
        flash('Acceso denegado. Solo personal técnico.', 'danger')
        return redirect(url_for('auth.dashboard'))

    id_tecnico = session['id_usuario']

    # --- PROCESAR EL CIERRE DE UNA OT (MÉTODO POST) ---
    if request.method == 'POST':
        id_ot = request.form.get('id_ot')
        id_equipo = request.form.get('id_equipo')
        diagnostico = request.form.get('diagnostico')
        nuevo_km = request.form.get('kilometraje')
        id_repuesto = request.form.get('id_repuesto')
        cantidad_repuesto = request.form.get('cantidad_repuesto')

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            # 1. Actualizar datos operativos del equipo (CU-08)
            if nuevo_km:
                cursor.execute("UPDATE equipos SET horas_uso = %s WHERE id_equipo = %s", (nuevo_km, id_equipo))
            
            # 2. Descontar repuesto si se utilizó uno (CU-S07)
            if id_repuesto and cantidad_repuesto:
                # Insertar en el detalle de la OT
                cursor.execute("INSERT INTO detalle_ot_repuestos (id_ot, id_repuesto, cantidad) VALUES (%s, %s, %s)", 
                               (id_ot, id_repuesto, cantidad_repuesto))
                # Restar del inventario
                cursor.execute("UPDATE repuestos SET stock_actual = stock_actual - %s WHERE id_repuesto = %s", 
                               (cantidad_repuesto, id_repuesto))

            # 3. Cerrar la Orden de Trabajo (CU-13)
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                UPDATE ordenes_trabajo 
                SET estado = 'Cerrada', diagnostico = %s, fecha_cierre = %s 
                WHERE id_ot = %s
            """, (diagnostico, fecha_actual, id_ot))

            # Si todo anduvo bien, consolidamos los cambios en el disco
            conexion.commit()
            flash('Orden de Trabajo cerrada y repuestos descontados exitosamente.', 'success')
        except Exception as e:
            # VITAL: Si cualquiera de las 3 operaciones falla, se deshace todo para no dejar datos corruptos
            conexion.rollback()
            flash(f'Error al procesar la OT: {str(e)}', 'danger')
        finally:
            conexion.close()

        # Patrón PRG: Limpia el POST para evitar ejecuciones dobles si el técnico refresca la pantalla
        return redirect(url_for('tecnico.mi_panel'))

    # --- LÓGICA PARA EL MÉTODO GET (Mostrar el panel de trabajo) ---
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Obtener las OTs asignadas a este técnico específico que no estén cerradas
        cursor.execute("""
            SELECT ot.id_ot, ot.id_equipo, e.codigo_patrimonial, e.nombre as equipo, 
                   ot.tipo_mantenimiento, ot.estado, ot.fecha_creacion, e.horas_uso
            FROM ordenes_trabajo ot
            INNER JOIN equipos e ON ot.id_equipo = e.id_equipo
            WHERE ot.id_tecnico = %s AND ot.estado != 'Cerrada'
            ORDER BY ot.fecha_creacion DESC
        """, (id_tecnico,))
        mis_ordenes = cursor.fetchall()

        # Obtener catálogo de repuestos con stock disponible para el select
        cursor.execute("SELECT id_repuesto, codigo_pieza, nombre, stock_actual FROM repuestos WHERE stock_actual > 0 ORDER BY nombre ASC")
        repuestos = cursor.fetchall()

    except Exception as e:
        mis_ordenes = []
        repuestos = []
        flash(f'Error al cargar las órdenes asignadas: {str(e)}', 'danger')
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()

    return render_template('tecnico_panel.html', ordenes=mis_ordenes, repuestos=repuestos)