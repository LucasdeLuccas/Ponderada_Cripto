# Usar uma imagem base oficial do Node
FROM node:16-alpine as build

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar o restante do código do frontend
COPY . .

# Construir o aplicativo para produção
RUN npm run build

# Usar uma imagem base do Nginx para servir o build
FROM nginx:stable-alpine

# Remover a configuração padrão do Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copiar os arquivos do build para o diretório padrão do Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Copiar a configuração personalizada do Nginx (opcional)
# COPY nginx.conf /etc/nginx/nginx.conf

# Expor a porta 80
EXPOSE 80

# Iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]
