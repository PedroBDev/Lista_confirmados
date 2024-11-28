import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'minha-chave-secreta')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql://usuario:senha@localhost:3306/base_de_dados')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
