# Usa a imagem base do Python
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o contêiner
COPY . .

# Expõe a porta usada pelo Flask
EXPOSE 3306

# Comando padrão para rodar o contêiner
CMD ["flask", "run", "--host=0.0.0.0"]
