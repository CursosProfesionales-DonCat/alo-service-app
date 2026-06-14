from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2.extras
from config import Config

cliente_bp = Blueprint('cliente', __name__)

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

@cliente_bp.route('/clientes', methods=['GET', 'POST'])
def gestionar_clientes():
    # Seguridad estricta: Solo Administrador (1) y Técnico (4)
    if 'id_usuario' not in session or session.get('id_rol') not in [1, 4]:
        flash('Acceso denegado. No tienes permisos para gestionar clientes.', 'danger')
        return redirect(url_for('auth.dashboard'))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == 'POST':
        accion = request.form.get('accion')

        # --- LÓGICA PARA NUEVO CLIENTE ---
        if accion == 'nuevo':
            razon_social = request.form.get('razon_social')
            ruc = request.form.get('ruc')
            contacto = request.form.get('contacto')
            tipo_cliente = request.form.get('tipo_cliente')

            try:
                sql = "INSERT INTO clientes (razon_social, ruc, contacto, tipo_cliente) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (razon_social, ruc, contacto, tipo_cliente))
                conexion.commit()
                flash('Cliente registrado exitosamente en la cartera.', 'success')
            except psycopg2.IntegrityError: # CORREGIDO: Excepción de Postgres
                conexion.rollback() # VITAL: Postgres exige rollback tras un error
                flash('Error: El número de RUC ya está registrado en el sistema.', 'danger')
            except Exception as e:
                conexion.rollback()
                flash(f'Error al registrar cliente: {str(e)}', 'danger')
                
            # Evita recarga duplicada de formulario al presionar F5
            return redirect(url_for('cliente.gestionar_clientes'))

        # --- LÓGICA PARA EDITAR CLIENTE ---
        elif accion == 'editar':
            id_cliente = request.form.get('id_cliente')
            razon_social = request.form.get('razon_social')
            ruc = request.form.get('ruc')
            contacto = request.form.get('contacto')
            tipo_cliente = request.form.get('tipo_cliente')

            try:
                sql = """UPDATE clientes 
                         SET razon_social = %s, ruc = %s, contacto = %s, tipo_cliente = %s 
                         WHERE id_cliente = %s"""
                cursor.execute(sql, (razon_social, ruc, contacto, tipo_cliente, id_cliente))
                conexion.commit()
                flash('Datos del cliente actualizados correctamente.', 'success')
            except psycopg2.IntegrityError:
                conexion.rollback()
                flash('Error: El número de RUC ingresado ya le pertenece a otro cliente.', 'danger')
            except Exception as e:
                conexion.rollback()
                flash(f'Error al actualizar cliente: {str(e)}', 'danger')
                
            return redirect(url_for('cliente.gestionar_clientes'))

    # Obtener la lista de clientes (Método GET)
    cursor.execute("SELECT * FROM clientes ORDER BY razon_social ASC")
    lista_clientes = cursor.fetchall()
    conexion.close()

    return render_template('clientes.html', clientes=lista_clientes)