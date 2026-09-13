# Define a imagem-base do container.
# Essa imagem contém uma instalação enxuta do Python 3.13
# sobre um pequeno sistema Linux.
FROM python:3.13-slim


# Impede o Python de criar arquivos temporários .pyc
# dentro do container.
ENV PYTHONDONTWRITEBYTECODE=1


# Faz o Python enviar os logs imediatamente para o terminal,
# sem mantê-los temporariamente em um buffer.
ENV PYTHONUNBUFFERED=1


# Define /app como o diretório de trabalho dentro do container.
# Os próximos comandos serão executados dentro dessa pasta.
WORKDIR /app


# Copia o arquivo de dependências do nosso computador
# para o diretório /app dentro da imagem.
COPY requirements.txt .


# Instala todas as bibliotecas registradas no requirements.txt.
# --no-cache-dir evita guardar arquivos de instalação desnecessários,
# ajudando a reduzir o tamanho da imagem.
RUN python -m pip install --no-cache-dir -r requirements.txt


# Copia a pasta app do computador para /app/app dentro da imagem.
# Essa pasta contém o código da nossa API.
COPY app ./app


# Documenta que a aplicação utiliza a porta 8000.
# EXPOSE não publica a porta automaticamente;
# a publicação será feita no comando docker run.
EXPOSE 8000


# Define o comando executado quando o container for iniciado.
#
# --host 0.0.0.0 permite que a API seja acessada
# de fora do container.
#
# Não usamos --reload dentro do container porque essa opção
# é destinada principalmente ao desenvolvimento local.
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
