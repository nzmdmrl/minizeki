FROM python:3.12-slim

# psycopg2 vb. derlemeler icin gerekli araclar
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# SQLite dosyasi burada durur (Coolify'da volume olarak baglanir)
RUN mkdir -p /data
ENV DATABASE_URL="sqlite:////data/minizeki.db"
ENV PORT=8420

EXPOSE 8420

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://localhost:8420/ || exit 1

CMD ["python", "main.py"]
