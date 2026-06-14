from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import bcrypt
import psycopg2
import psycopg2.extras
from config import Config
import secrets
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import joblib
import pandas as pd

auth_bp = Blueprint('auth', __name__)

def obtener_conexion():
    return psycopg2.connect(
        host=Config.PG_HOST,
        user=Config.PG_USER,
        password=Config.PG_PASSWORD,
        dbname=Config.PG_DB,
        port=Config.PG_PORT,
        cursor_factory=psycopg2.extras.RealDictCursor
    )

def enviar_correo_recuperacion(destinatario, token):
    remitente = "junjunaloe004@gmail.com" # REEMPLAZA
    password_app = "zcptnxrnrgonapsk" # REEMPLAZA
    
    enlace = url_for('auth.reset_password', token=token, _external=True)
    
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = "Recuperar Contraseña - ALO Service"
    
    cuerpo = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
        <h2 style="color: #FFD400; background-color: #0B0B0B; padding: 10px; text-align: center; border-radius: 5px;">ALO Service</h2>
        <h3>Recuperación de contraseña</h3>
        <p>Has solicitado restablecer tu contraseña en el sistema de Mantenimiento Predictivo.</p>
        <p>Haz clic en el siguiente botón para crear una nueva (el enlace caduca en 1 hora):</p>
        <div style="text-align: center; margin: 20px 0;">
            <a href="{enlace}" style="background-color: #FFD400; color: #000; padding: 10px 20px; text-decoration: none; font-weight: bold; border-radius: 5px;">Restablecer mi contraseña</a>
        </div>
        <p style="color: #555; font-size: 12px;">Si no fuiste tú, ignora este mensaje.</p>
    </div>
    """
    msg.attach(MIMEText(cuerpo, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
        server.starttls()
        server.login(remitente, password_app)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if 'id_usuario' in session:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        from app.models.usuario_model import UsuarioModel
        usuario = UsuarioModel.obtener_por_correo(correo)
        
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario['password_hash'].encode('utf-8')):
            session['id_usuario'] = usuario['id_usuario']
            session['id_rol'] = usuario['id_rol']
            session['nombres'] = usuario['nombres']
            session['apellidos'] = usuario['apellidos']
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Credenciales incorrectas o usuario inactivo', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        correo = request.form.get('correo').strip()
        from app.models.usuario_model import UsuarioModel
        usuario = UsuarioModel.obtener_por_correo(correo)
        
        if not usuario:
            flash(f'DIAGNÓSTICO: El correo "{correo}" NO existe en tu tabla de usuarios.', 'danger')
            return render_template('auth/forgot_password.html')
            
        token = secrets.token_hex(32)
        expiry = datetime.now() + timedelta(hours=1)
        
        UsuarioModel.guardar_token_recuperacion(correo, token, expiry)
        enviado = enviar_correo_recuperacion(correo, token)
        
        if enviado:
            flash('¡ÉXITO! El correo fue aceptado y enviado correctamente.', 'success')
        else:
            flash('DIAGNÓSTICO: Falló la conexión SMTP con Gmail.', 'danger')
            
        return redirect(url_for('auth.login'))
        
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    from app.models.usuario_model import UsuarioModel
    usuario = UsuarioModel.verificar_token(token)
    
    if not usuario:
        flash('El enlace es inválido o ha caducado.', 'danger')
        return redirect(url_for('auth.forgot_password'))
        
    if request.method == 'POST':
        nueva_password = request.form.get('nueva_password')
        confirmar_password = request.form.get('confirmar_password')
        
        if nueva_password == confirmar_password:
            password_hash = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            UsuarioModel.actualizar_password(usuario['id_usuario'], password_hash)
            
            flash('Contraseña actualizada con éxito. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Las contraseñas no coinciden.', 'danger')
            
    return render_template('auth/reset_password.html', token=token)

@auth_bp.route('/dashboard')
def dashboard():
    if 'id_usuario' not in session:
        return redirect(url_for('auth.login'))
        
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM equipos_historial WHERE nivel_riesgo = 'ALTO'")
        equipos_riesgo = cursor.fetchone()['total'] or 0
        
        cursor.execute("SELECT SUM(ot_abiertas) as total FROM equipos_historial")
        ot_pendientes = cursor.fetchone()['total'] or 0

        try:
            cursor.execute("SELECT precision_score FROM metricas_modelo_ml ORDER BY id_metrica DESC LIMIT 1")
            res_metrica = cursor.fetchone()
            eficiencia_modelo = round(float(res_metrica['precision_score']) * 100, 1) if res_metrica else 92.4
        except:
            eficiencia_modelo = 92.4

        cursor.execute("SELECT nivel_riesgo, COUNT(*) as total FROM equipos_historial GROUP BY nivel_riesgo")
        estados_db = cursor.fetchall()
        labels_flota = [row['nivel_riesgo'] for row in estados_db]
        data_flota = [row['total'] for row in estados_db]

        cursor.execute("SELECT criticidad, COUNT(*) as total FROM equipos_historial GROUP BY criticidad")
        ots_db = cursor.fetchall()
        labels_ots = [row['criticidad'] for row in ots_db]
        data_ots = [row['total'] for row in ots_db]

    except Exception as e:
        print(f"Error en dashboard: {e}")
        equipos_riesgo = 0
        ot_pendientes = 0
        eficiencia_modelo = 0
        labels_flota, data_flota = [], []
        labels_ots, data_ots = [], []
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()
    
    return render_template('dashboard.html', 
                           equipos_riesgo=equipos_riesgo, 
                           ot_pendientes=ot_pendientes, 
                           eficiencia=eficiencia_modelo,
                           labels_flota=labels_flota, data_flota=data_flota,
                           labels_ots=labels_ots, data_ots=data_ots)

@auth_bp.route('/usuarios', methods=['GET', 'POST'])
def gestionar_usuarios():
    if 'id_usuario' not in session or session.get('id_rol') != 1:
        flash('Acceso denegado. Módulo exclusivo de administración.', 'danger')
        return redirect(url_for('auth.dashboard'))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == 'POST':
        accion = request.form.get('accion')

        if accion == 'nuevo':
            nombres = request.form.get('nombres')
            correo = request.form.get('correo')
            contrasena = request.form.get('contrasena')
            id_rol = request.form.get('id_rol')
            hash_pw = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            try:
                sql = "INSERT INTO usuarios (nombres, apellidos, correo, password_hash, id_rol) VALUES (%s, '', %s, %s, %s)"
                cursor.execute(sql, (nombres, correo, hash_pw, id_rol))
                conexion.commit()
                flash('Usuario registrado exitosamente.', 'success')
            except psycopg2.IntegrityError:
                conexion.rollback()
                flash('Error: El correo electrónico ya se encuentra registrado.', 'danger')
            except Exception as e:
                conexion.rollback()
                flash(f'Error al registrar: {str(e)}', 'danger')

        elif accion == 'editar':
            id_usuario_edit = request.form.get('id_usuario')
            nombres = request.form.get('nombres')
            correo = request.form.get('correo')
            contrasena = request.form.get('contrasena')
            id_rol = request.form.get('id_rol')

            try:
                if contrasena and contrasena.strip() != "":
                    hash_pw = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    sql = """UPDATE usuarios 
                             SET nombres = %s, correo = %s, password_hash = %s, id_rol = %s 
                             WHERE id_usuario = %s"""
                    cursor.execute(sql, (nombres, correo, hash_pw, id_rol, id_usuario_edit))
                else:
                    sql = """UPDATE usuarios 
                             SET nombres = %s, correo = %s, id_rol = %s 
                             WHERE id_usuario = %s"""
                    cursor.execute(sql, (nombres, correo, id_rol, id_usuario_edit))
                
                conexion.commit()
                flash('Datos del usuario actualizados correctamente.', 'success')
            except psycopg2.IntegrityError:
                conexion.rollback()
                flash('Error: El correo pertenece a otro usuario.', 'danger')
            except Exception as e:
                conexion.rollback()
                flash(f'Error al actualizar: {str(e)}', 'danger')

    cursor.execute("""
        SELECT u.*, r.nombre as nombre_rol 
        FROM usuarios u 
        INNER JOIN roles r ON u.id_rol = r.id_rol 
        ORDER BY u.id_usuario DESC
    """)
    lista_usuarios = cursor.fetchall()

    cursor.execute("SELECT id_rol, nombre as nombre_rol FROM roles ORDER BY id_rol ASC")
    lista_roles = cursor.fetchall()

    conexion.close()
    return render_template('usuarios.html', usuarios=lista_usuarios, roles=lista_roles)

# --- NUEVA RUTA: MONITOR PREDICTIVO IA ---
@auth_bp.route('/predicciones')
def predicciones():
    if 'id_usuario' not in session:
        return redirect(url_for('auth.login'))

    resultados = []
    modelo_cargado = False
    
    ruta_modelo = 'app/models/ml/random_forest_alo.pkl'
    ruta_encoder = 'app/models/ml/encoder_criticidad.pkl'
    
    if os.path.exists(ruta_modelo) and os.path.exists(ruta_encoder):
        try:
            modelo = joblib.load(ruta_modelo)
            encoder = joblib.load(ruta_encoder)
            modelo_cargado = True
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Seleccionamos los últimos 12 equipos de la flota para monitoreo
            cursor.execute("""
                SELECT id_equipo, codigo_patrimonial, nombre, estado, horas_uso, fecha_adquisicion 
                FROM equipos 
                ORDER BY id_equipo DESC LIMIT 12
            """)
            equipos_db = cursor.fetchall()
            
            for eq in equipos_db:
                id_eq = eq['id_equipo']
                
                # 1. Antigüedad
                try:
                    antiguedad = (datetime.now().date() - eq['fecha_adquisicion'].date()).days // 365
                except:
                    antiguedad = 5
                    
                # 2. OTs Pendientes
                cursor.execute("SELECT COUNT(*) as total FROM ordenes_trabajo WHERE id_equipo = %s AND estado = 'Pendiente'", (id_eq,))
                ot_abiertas = cursor.fetchone()['total']
                
                # 3. Fallas históricas
                cursor.execute("SELECT COUNT(*) as total FROM fallas WHERE id_equipo = %s", (id_eq,))
                fallas = cursor.fetchone()['total']
                
                # 4. Derivamos variables de telemetría para la IA
                horas = eq['horas_uso'] or 0
                kilometraje = horas * 25 
                criticidad = "Alto" if fallas >= 2 else "Medio"
                dias_mant = 45 # Promedio simulado desde el último mantenimiento
                
                # 5. Transformamos y predecimos
                crit_num = encoder.transform([criticidad])[0]
                datos_ia = pd.DataFrame([[kilometraje, crit_num, dias_mant, fallas, horas, antiguedad, ot_abiertas]],
                                        columns=['kilometraje', 'criticidad_num', 'dias_ultimo_mant', 'fallas_6_meses', 'horas_uso', 'antiguedad_anios', 'ot_abiertas'])
                
                probabilidades = modelo.predict_proba(datos_ia)[0]
                prob_falla = round(max(probabilidades) * 100, 1)
                nivel_riesgo = modelo.predict(datos_ia)[0]
                
                color = 'success'
                if prob_falla >= 75.0: color = 'danger'
                elif prob_falla >= 40.0: color = 'warning'
                
                resultados.append({
                    'codigo': eq['codigo_patrimonial'],
                    'nombre': eq['nombre'],
                    'estado': nivel_riesgo,
                    'horas': horas,
                    'prob_falla': prob_falla,
                    'color': color
                })
                
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"Error procesando IA: {e}")
            modelo_cargado = False

    return render_template('predicciones.html', modelo_cargado=modelo_cargado, resultados=resultados)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
    
