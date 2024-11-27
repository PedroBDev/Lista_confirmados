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
        quantidade = request.form.get("senhas")

        # Verifica se todos os campos foram preenchidos
        if not nome or not confirmacao or not quantidade:
            flash("Todos os campos são obrigatórios!", "error")
            return redirect(url_for("index"))

        try:
            # Converte a quantidade para inteiro
            quantidade = int(quantidade)
        except ValueError:
            flash("A quantidade de senhas deve ser um número!", "error")
            return redirect(url_for("index"))

        # Cria o dicionário com os dados
        nova_confirmacao = {
            "nome": nome,
            "presenca": confirmacao,
            "quantidade": quantidade
        }

        # Carrega as confirmações existentes
        try:
            if os.path.exists(CAMINHO_ARQUIVO):
                with open(CAMINHO_ARQUIVO, "r") as arquivo:
                    lista_confirmacoes = json.load(arquivo)
            else:
                lista_confirmacoes = []
        except json.JSONDecodeError:
            lista_confirmacoes = []

        # Adiciona a nova confirmação
        lista_confirmacoes.append(nova_confirmacao)

        # Salva a lista atualizada
        try:
            with open(CAMINHO_ARQUIVO, "w") as arquivo:
                json.dump(lista_confirmacoes, arquivo, indent=2)
        except Exception as e:
            flash(f"Erro ao salvar as confirmações: {e}", "error")
            return redirect(url_for("index"))

        # Exibe uma mensagem de sucesso
        flash("Sua confirmação foi registrada com sucesso!", "success")

        # Redireciona para a página de agradecimento
        return redirect(url_for("obrigado"))

    return render_template("index.html")

@app.route("/agradecimento", methods=["GET"])
def obrigado():
    return render_template("obrigado.html")



@app.route('/lista')
def lista():
    total_confirmados = 0
    try:
        # Tenta abrir o arquivo
        with open(CAMINHO_ARQUIVO, 'r') as arquivo:
            # Verifica se o arquivo está vazio
            conteudo = arquivo.read().strip()
            if conteudo:
                lista_json = json.loads(conteudo)
            else:
                lista_json = []  # Se estiver vazio, cria uma lista vazia
    except FileNotFoundError:
        # Se o arquivo não existir, cria uma lista vazia
        lista_json = []
    except json.JSONDecodeError:
        # Se o arquivo estiver corrompido ou inválido
        flash("Erro ao carregar lista de confirmações. O arquivo pode estar corrompido.", "error")
        return redirect(url_for('index'))

    # Contar o total de confirmados (presença == "sim")
    for item in lista_json:
        if item['presenca'] == 'sim':
            total_confirmados += item['quantidade']

    return render_template("lista.html", lista=lista_json, total_confirmados=total_confirmados)





