from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Criação do objeto app e do db
app = Flask(__name__)
app.config.from_object('config.Config')  # Configuração do Flask
db = SQLAlchemy(app)  # Inicializa o SQLAlchemy

def create_app():
    # Aqui você importa as rotas e os modelos dentro da função de criação
    from . import routes, models
    return app  # Retorna o objeto app, após as importações











