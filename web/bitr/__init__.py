from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
#from flask_talisman import Talisman

import locale

#Crear una extension
db = SQLAlchemy()

def create_app():

    #Crear la app
    app = Flask(__name__)

    #Forzar https
    #Talisman(app)

    #Configuracion del proyecto
    app.config.from_object('config.Config')
    
    #Inicializar db
    db.init_app(app)

    #Inicializar CKEditor(Para insertar textos)
    ckeditor = CKEditor(app)

    #Configurar idioma
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

    #Registrar los blueprint
    from bitr import auth
    app.register_blueprint(auth.bp)

    from bitr import videoanalisis
    app.register_blueprint(videoanalisis.bp)

    from bitr import dashboards
    app.register_blueprint(dashboards.bp)

    from bitr import interfaces
    app.register_blueprint(interfaces.bp)

    from bitr import eventos
    app.register_blueprint(eventos.bp)

    #Pagina principal
    @app.route('/')
    def index():
        return render_template('index.html')
    
    #Crear esquema de tablas luego de definir todos los modelos con SQLAlchemy
    with app.app_context():
        db.create_all()
    
    return app