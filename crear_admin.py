import bcrypt
import psycopg2
from config import Config

# Encriptar la contraseña "admin123"
password_plana = b"admin123"
password_hash = bcrypt.hashpw(password_plana, bcrypt.gensalt()).decode('utf-8')

print("⏳ Conectando a PostgreSQL para inicializar administrador...")

try:
    # Conectar usando las credenciales de Postgres
    conexion = psycopg2.connect(
        host=Config.PG_HOST,
        user=Config.PG_USER,
        password=Config.PG_PASSWORD,
        dbname=Config.PG_DB,
        port=Config.PG_PORT
    )
    cursor = conexion.cursor()

    # id_rol = 1 (Administrador)
    sql = """INSERT INTO usuarios (id_rol, nombres, apellidos, correo, password_hash) 
             VALUES (1, 'Carlos', 'Li Chocano', 'admin@alo.com', %s)"""
    
    cursor.execute(sql, (password_hash,))
    conexion.commit()
    print("✅ Usuario administrador creado con éxito en PostgreSQL: admin@alo.com / Clave: admin123")

except Exception as e:
    # VITAL: Si falla por duplicado, hacemos rollback para limpiar el estado de la conexión
    if 'conexion' in locals() and conexion:
        conexion.rollback()
    print(f"❌ Error (quizás ya ejecutaste este script antes o la tabla está vacía): {e}")

finally:
    if 'conexion' in locals() and conexion:
        conexion.close()
        print("🔌 Conexión cerrada de forma segura.")