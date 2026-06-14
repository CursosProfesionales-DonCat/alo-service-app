from flask import Flask
import os
import webbrowser
from threading import Timer

app = Flask(__name__, 
            template_folder=os.path.join('app', 'views', 'templates'),
            static_folder=os.path.join('app', 'views', 'static'))

app.config.from_object('config.Config')

# -----------------------------------------------------
# REGISTRO DE CONTROLADORES (¡Solo una vez por cada uno!)
# -----------------------------------------------------
from app.controllers.auth_controller import auth_bp
app.register_blueprint(auth_bp)

from app.controllers.predict_controller import predict_bp
app.register_blueprint(predict_bp)

from app.controllers.admin_controller import admin_bp
app.register_blueprint(admin_bp)

from app.controllers.equipo_controller import equipo_bp
app.register_blueprint(equipo_bp)

from app.controllers.ordenes_controller import ordenes_bp
app.register_blueprint(ordenes_bp)

# ---- AQUÍ ESTÁ EL CONTROLADOR FALTANTE ----
from app.controllers.inventario_controller import inventario_bp
app.register_blueprint(inventario_bp)
# -----------------------------------------------------

from app.controllers.tecnico_controller import tecnico_bp
app.register_blueprint(tecnico_bp)

from app.controllers.cliente_controller import cliente_bp
app.register_blueprint(cliente_bp)

from app.controllers.analista_controller import analista_bp
app.register_blueprint(analista_bp)

from app.controllers.reportes_controller import reportes_bp
app.register_blueprint(reportes_bp)

def abrir_navegador():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        Timer(1, abrir_navegador).start()
        
    app.run(debug=True, port=5000)