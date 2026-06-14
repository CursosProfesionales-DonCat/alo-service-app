from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2.extras
from config import Config

equipo_bp = Blueprint('equipo', __name__)

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

@equipo_bp.route('/equipos', methods=['GET', 'POST'])
def gestionar_equipos():
    if 'id_usuario' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        codigo = request.form.get('codigo_patrimonial')
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        id_cliente = request.form.get('id_cliente')
        
        # Validar si no se seleccionó ningún cliente de la lista
        id_cliente = None if id_cliente == "" else id_cliente

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            sql = """INSERT INTO equipos (codigo_patrimonial, nombre, tipo, estado, horas_uso, id_cliente) 
                     VALUES (%s, %s, %s, 'Operativo', 0, %s)"""
            cursor.execute(sql, (codigo, nombre, tipo, id_cliente))
            conexion.commit()
            flash('Equipo registrado correctamente y vinculado al cliente.', 'success')
        except psycopg2.IntegrityError:
            conexion.rollback() # VITAL: Libera la transacción en Postgres si el código patrimonial está duplicado
            flash('Error: El código patrimonial ya se encuentra registrado en el sistema.', 'danger')
        except Exception as e:
            conexion.rollback()
            flash(f'Error al registrar equipo: {str(e)}', 'danger')
        finally:
            conexion.close()

        # Patrón PRG: Redirección para limpiar el POST y evitar registros dobles en la base de datos
        return redirect(url_for('equipo.gestionar_equipos'))

    # --- LÓGICA PARA EL MÉTODO GET (Mostrar la vista de equipos) ---
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Obtener los equipos incluyendo la Razón Social del cliente (LEFT JOIN)
        query_equipos = """
            SELECT e.*, c.razon_social as cliente 
            FROM equipos e
            LEFT JOIN clientes c ON e.id_cliente = c.id_cliente
            WHERE e.estado != 'Inactivo'
            ORDER BY e.id_equipo DESC
        """
        cursor.execute(query_equipos)
        lista_equipos = cursor.fetchall()

        # Obtener el catálogo de clientes para poblar el elemento <select> del formulario
        cursor.execute("SELECT id_cliente, razon_social FROM clientes ORDER BY razon_social ASC")
        lista_clientes = cursor.fetchall()
        
    except Exception as e:
        lista_equipos = []
        lista_clientes = []
        flash(f'Error al cargar el catálogo de flota: {str(e)}', 'danger')
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()

    return render_template('equipos.html', equipos=lista_equipos, clientes=lista_clientes)