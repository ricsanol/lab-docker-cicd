# Utiliza uma imagem compacta do servidor Nginx.
FROM nginx:alpine

# Substitui a configuração padrão pela configuração do laboratório.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos do dashboard para o diretório público.
COPY index.html /usr/share/nginx/html/index.html
COPY styles.css /usr/share/nginx/html/styles.css
COPY app.js /usr/share/nginx/html/app.js

# Documenta a porta utilizada pelo Nginx.
EXPOSE 80

# Verifica se o dashboard está respondendo.
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1/ || exit 1