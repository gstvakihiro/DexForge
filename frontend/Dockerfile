# Imagem base: Node enxuta
FROM node:22-slim

WORKDIR /app

# Copia só os arquivos de dependência primeiro (mesmo motivo do backend:
# cache de layer, builds mais rápidos)
COPY package.json package-lock.json ./
RUN npm install

# Agora copia o resto do código
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
