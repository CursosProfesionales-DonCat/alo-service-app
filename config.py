import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta_local_por_si_acaso')
    PG_HOST = os.environ.get('PG_HOST', 'localhost')
    PG_USER = os.environ.get('PG_USER', 'postgres')
    PG_PASSWORD = os.environ.get('PG_PASSWORD', 'tu_clave_local')
    PG_DB = os.environ.get('PG_DB', 'alo_service')
    PG_PORT = os.environ.get('PG_PORT', '5432')
    
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'app', 'ml_core', 'modelo_mantenimiento.pkl')