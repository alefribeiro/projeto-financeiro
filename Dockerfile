# Dockerfile

# Usa uma imagem base Python
FROM python:3.12-slim-bookworm

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o container
COPY . .

# Expõe a porta que o Django vai usar (se estiver rodando o servidor web)
EXPOSE 8000

# Comando padrão para iniciar o Django (pode ser sobrescrito pelo docker-compose)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]