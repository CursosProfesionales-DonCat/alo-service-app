import psycopg2
import psycopg2.extras
from config import Config


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

class UsuarioModel:
    @staticmethod
    def obtener_por_correo(correo):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                # La sintaxis de paso de parámetros (%s) es idéntica en Postgres
                cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND estado = TRUE", (correo,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener el usuario en el modelo: {e}")
            return None
        finally:
            if 'conexion' in locals() and conexion:
                conexion.close()



# Agrega estos métodos dentro de tu class UsuarioModel:

    @staticmethod
    def guardar_token_recuperacion(correo, token, expiry):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    UPDATE usuarios 
                    SET reset_token = %s, token_expiry = %s 
                    WHERE correo = %s
                """, (token, expiry, correo))
                conexion.commit()
                return cursor.rowcount > 0 # Retorna True si encontró el correo
        except Exception as e:
            conexion.rollback()
            return False
        finally:
            if 'conexion' in locals() and conexion:
                conexion.close()

    @staticmethod
    def verificar_token(token):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                # Compara que el token exista y no haya expirado
                cursor.execute("""
                    SELECT * FROM usuarios 
                    WHERE reset_token = %s AND token_expiry > CURRENT_TIMESTAMP
                """, (token,))
                return cursor.fetchone()
        finally:
            if 'conexion' in locals() and conexion:
                conexion.close()

    @staticmethod
    def actualizar_password(id_usuario, password_hash):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                # Actualiza la clave y limpia los tokens por seguridad
                cursor.execute("""
                    UPDATE usuarios 
                    SET password_hash = %s, reset_token = NULL, token_expiry = NULL 
                    WHERE id_usuario = %s
                """, (password_hash, id_usuario))
                conexion.commit()
        finally:
            if 'conexion' in locals() and conexion:
                conexion.close()


        