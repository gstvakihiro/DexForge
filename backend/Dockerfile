# Imagem base: Python enxuta
FROM python:3.13-slim

WORKDIR /app

# Instala dependências do sistema necessárias pro psycopg2 e afins
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia só o requirements primeiro — assim o Docker reaproveita esse "layer"
# em cache quando só o código mudar (não as dependências), tornando builds
# futuros bem mais rápidos.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Agora copia o resto do código
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
