from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2.extras
from config import Config

inventario_bp = Blueprint('inventario', __name__)

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

@inventario_bp.route('/inventario', methods=['GET', 'POST'])
def gestionar_inventario():
    # Seguridad: Admin (1), Supervisor (3) y Enc. Almacén (5)
    if 'id_usuario' not in session or session.get('id_rol') not in [1, 3, 5]:
        flash('Acceso denegado. Módulo exclusivo de logística.', 'danger')
        return redirect(url_for('auth.dashboard'))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == 'POST':
        accion = request.form.get('accion')

        # --- LÓGICA PARA CATALOGAR NUEVA PIEZA ---
        if accion == 'nuevo':
            codigo_pieza = request.form.get('codigo_pieza')
            nombre = request.form.get('nombre')
            stock_actual = request.form.get('stock_actual', 0)
            stock_minimo = request.form.get('stock_minimo', 0)

            try:
                sql = "INSERT INTO repuestos (codigo_pieza, nombre, stock_actual, stock_minimo) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (codigo_pieza, nombre, stock_actual, stock_minimo))
                conexion.commit()
                flash('Repuesto catalogado exitosamente.', 'success')
            except psycopg2.IntegrityError:
                conexion.rollback() # VITAL: Libera el bloque de transacción en Postgres
                flash('Error: El código de pieza ya se encuentra registrado.', 'danger')
            except Exception as e:
                conexion.rollback()
                flash(f'Error al registrar repuesto: {str(e)}', 'danger')
            finally:
                conexion.close()
            
            return redirect(url_for('inventario.gestionar_inventario'))

        # --- LÓGICA PARA EDITAR PIEZA EXISTENTE ---
        elif accion == 'editar':
            id_repuesto = request.form.get('id_repuesto')
            codigo_pieza = request.form.get('codigo_pieza')
            nombre = request.form.get('nombre')
            stock_actual = request.form.get('stock_actual')
            stock_minimo = request.form.get('stock_minimo')

            try:
                sql = """UPDATE repuestos 
                         SET codigo_pieza = %s, nombre = %s, stock_actual = %s, stock_minimo = %s 
                         WHERE id_repuesto = %s"""
                cursor.execute(sql, (codigo_pieza, nombre, stock_actual, stock_minimo, id_repuesto))
                conexion.commit()
                flash('Catálogo de repuesto actualizado correctamente.', 'success')
            except psycopg2.IntegrityError:
                conexion.rollback()
                flash('Error: El código de pieza ya pertenece a otro repuesto.', 'danger')
            except Exception as e:
                conexion.rollback()
                flash(f'Error al actualizar repuesto: {str(e)}', 'danger')
            finally:
                conexion.close()
                
            return redirect(url_for('inventario.gestionar_inventario'))

        # --- LÓGICA PARA INGRESAR NUEVO STOCK (BOTÓN AZUL) ---
        elif accion == 'ingresar':
            id_repuesto = request.form.get('id_repuesto')
            cantidad = int(request.form.get('cantidad', 0))

            try:
                sql = "UPDATE repuestos SET stock_actual = stock_actual + %s WHERE id_repuesto = %s"
                cursor.execute(sql, (cantidad, id_repuesto))
                conexion.commit()
                flash(f'Se agregaron {cantidad} unidades al inventario correctamente.', 'success')
            except Exception as e:
                conexion.rollback()
                flash(f'Error al ingresar stock: {str(e)}', 'danger')
            finally:
                conexion.close()
                
            return redirect(url_for('inventario.gestionar_inventario'))

    # Obtener el inventario completo (Método GET)
    try:
        cursor.execute("SELECT * FROM repuestos ORDER BY id_repuesto DESC")
        lista_repuestos = cursor.fetchall()
    except Exception as e:
        lista_repuestos = []
        flash(f'Error al cargar el inventario: {str(e)}', 'danger')
    finally:
        conexion.close()

    return render_template('inventario.html', repuestos=lista_repuestos)