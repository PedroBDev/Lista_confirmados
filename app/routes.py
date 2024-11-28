from flask import render_template, request, redirect, url_for, flash
from . import db, app# Importando o db, mas não o app
from .models import Confirmacao  # Importa o modelo de confirmação
from flask_sqlalchemy import SQLAlchemy

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        presenca = request.form.get('presenca')
        senhas = request.form.get('senhas')

        if not nome or not presenca or not senhas:
            flash('Todos os campos precisam ser preenchidos')
            return redirect(url_for("index"))

        # Converte 'senhas' para inteiro (caso necessário)
        try:
            senhas = int(senhas)  # Converte para inteiro, caso contrário, causaria um erro
        except ValueError:
            flash('O campo "senhas" precisa ser um número inteiro.')
            return redirect(url_for("index"))

        confirmacao = Confirmacao(nome=nome, presenca=presenca, senha=senhas)
        db.session.add(confirmacao)
        db.session.commit()

        return redirect(url_for("obrigado"))

    return render_template('index.html')

@app.route('/agradecimento')
def obrigado():
    return render_template('obrigado.html')

@app.route('/lista')
def lista():
    #contando a quantidade de confirmados

    total_senhas = db.session.query(db.func.sum(Confirmacao.senha)).filter_by(presenca="sim").scalar()

    if total_senhas is None:
        total_senhas=0


    #listando os dados

    confirmacoes= db.session.query(Confirmacao).all()


    return render_template('lista.html', confirmacoes=confirmacoes, total_senhas=total_senhas)


