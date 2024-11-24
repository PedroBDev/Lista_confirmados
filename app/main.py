# Rota para a página principal
from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
app = Flask(__name__)

app.secret_key = os.urandom(24)

# Definindo o caminho da pasta 'data' e o nome do arquivo JSON
CAMINHO_DIRETORIO = os.path.join(os.getcwd(), 'data')  # Obtém o caminho absoluto da pasta 'data'
CAMINHO_ARQUIVO = os.path.join(CAMINHO_DIRETORIO, 'confirmacoes.json')  # Junta com o nome do arquivo

# Cria a pasta 'data' caso ela não exista
if not os.path.exists(CAMINHO_DIRETORIO):
    os.makedirs(CAMINHO_DIRETORIO)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Captura os dados do formulário
        nome = request.form.get("nome")
        confirmacao = request.form.get("presenca")

        if not nome or not confirmacao:
            flash("Todos os campos são obrigatórios!", "error")
            return redirect(url_for("index"))

        # Cria o dicionário com os dados
        nova_confirmacao = {"nome": nome, "presenca": confirmacao}

        # Carrega as confirmações existentes
        try:
            with open(CAMINHO_ARQUIVO, "r") as arquivo:
                lista_confirmacoes = json.load(arquivo)
        except FileNotFoundError:
            lista_confirmacoes = []

        # Adiciona a nova confirmação
        lista_confirmacoes.append(nova_confirmacao)

        # Salva a lista atualizada
        with open(CAMINHO_ARQUIVO, "w") as arquivo:
            json.dump(lista_confirmacoes, arquivo, indent=2)

        # Exibe uma mensagem de sucesso
        flash("Sua confirmação foi registrada com sucesso!", "success")

        # Redireciona para a página de agradecimento
        return redirect(url_for("obrigado"))

    return render_template("index.html")

@app.route("/agradecimento", methods=["POST"])
def obrigado():
    return render_template("obrigado.html")



@app.route('/lista')
def lista():
    try:
        with open(CAMINHO_ARQUIVO, 'r') as arquivo:
            lista_json = json.load(arquivo)
    except FileNotFoundError:
        flash("Erro ao carregar lista", "error")
        return redirect(url_for('index'))

    # Contar o total de confirmados (presença == "sim")
    total_confirmados = sum(1 for item in lista_json if item['presenca'] == 'sim')

    return render_template("lista.html", lista=lista_json, total_confirmados=total_confirmados)





# Inicializa o aplicativo
if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    app.run(host='0.0.0.0', port = port)
