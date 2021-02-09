from flask import Flask

from .config import Config
from .extensions import db, migrate

from .usuarios.model import Usuarios
from .pagamentos.model import Pagamentos

from .usuarios.controllers import usuario_api
from .produtos.controllers import produtos_api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)

    app.register_blueprint(usuario_api)
    app.register_blueprint(produtos_api)

    return app