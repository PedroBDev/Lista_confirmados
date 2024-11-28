from app import db

class Confirmacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    presenca = db.Column(db.String(3))
    senha = db.Column(db.Integer)

    def __init__(self, nome, presenca, senha):
        self.nome = nome
        self.presenca = presenca
        self.senha = senha



