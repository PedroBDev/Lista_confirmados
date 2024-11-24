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

# Rota para a página principal
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/agradecimento", methods=['POST'])
def obrigado():
    try:
        # Captura os dados do formulário
        nome = request.form.get('nome')
        confirmacao = request.form.get('presenca')

        if not nome or not confirmacao:
            flash("Por favor, preencha todos os campos!", "error")
            return redirect(url_for('index'))

        # Cria o dicionário com os dados
        dict = {'nome': nome, 'presenca': confirmacao}

        # Tenta carregar os dados existentes no arquivo JSON
        if os.path.exists(CAMINHO_ARQUIVO) and os.path.getsize(CAMINHO_ARQUIVO) > 0:
            with open(CAMINHO_ARQUIVO, 'r') as arquivo:
                lista_json = json.load(arquivo)
        else:
            lista_json = []  # Se o arquivo não existir ou estiver vazio, começa com uma lista vazia

        # Adiciona o novo dicionário à lista
        lista_json.append(dict)

        # Salva a lista de volta no arquivo JSON
        with open(CAMINHO_ARQUIVO, 'w') as arquivo:
            json.dump(lista_json, arquivo, indent=2)

        flash("Sua confirmação foi registrada com sucesso!", "success")
        return redirect(url_for('obrigado_page'))

    except Exception as e:
        flash(f"Ocorreu um erro ao processar sua confirmação: {str(e)}", "error")
        return redirect(url_for('index'))


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
    app.run(debug=True)
