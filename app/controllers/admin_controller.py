from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import bcrypt
import psycopg2
import psycopg2.extras
from config import Config

admin_bp = Blueprint('admin', __name__)

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

@admin_bp.route('/usuarios', methods=['GET', 'POST'])
def gestionar_usuarios():
    # Restricción de seguridad: Solo el Administrador (id_rol = 1) puede acceder
    if 'id_usuario' not in session or session.get('id_rol') != 1:
        flash('Acceso denegado. Se requieren permisos de Administrador.', 'danger')
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        correo = request.form.get('correo')
        password = request.form.get('password')
        id_rol = request.form.get('id_rol')

        # Encriptar contraseña con Bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            sql = """INSERT INTO usuarios (id_rol, nombres, apellidos, correo, password_hash) 
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (id_rol, nombres, apellidos, correo, password_hash))
            conexion.commit()
            flash('Usuario creado exitosamente.', 'success')
        except psycopg2.IntegrityError: # CORREGIDO: Excepción de Postgres
            conexion.rollback() # VITAL: Libera la transacción bloqueada
            flash('El correo electrónico ya se encuentra registrado.', 'danger')
        except Exception as e:
            conexion.rollback()
            flash(f'Error al crear el usuario: {str(e)}', 'danger')
        finally:
            conexion.close()
            
        # Redirección para limpiar la petición POST y evitar envíos dobles al recargar
        return redirect(url_for('admin.gestionar_usuarios'))

    # --- LÓGICA PARA EL MÉTODO GET (Mostrar la vista) ---
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Obtener lista de usuarios y roles para mostrarlos en la vista
        cursor.execute("""
            SELECT u.id_usuario, u.nombres, u.apellidos, u.correo, u.estado, r.nombre as rol 
            FROM usuarios u 
            INNER JOIN roles r ON u.id_rol = r.id_rol
            ORDER BY u.id_usuario DESC
        """)
        lista_usuarios = cursor.fetchall()

        cursor.execute("SELECT * FROM roles ORDER BY id_rol ASC")
        lista_roles = cursor.fetchall()
        
    except Exception as e:
        lista_usuarios = []
        lista_roles = []
        flash(f'Error al cargar los datos: {str(e)}', 'danger')
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()

    return render_template('usuarios.html', usuarios=lista_usuarios, roles=lista_roles)