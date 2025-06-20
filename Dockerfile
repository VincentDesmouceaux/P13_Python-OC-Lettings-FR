# Dockerfile ----------------------------------------------------------
FROM python:3.12-slim

# 1. ENV de base (pas les secrets !) 
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# 2. Dépendances
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 3. Code source
COPY . .

# 4. Port exposé
EXPOSE 8000

# 5. Commande – on laisse la charge à python-dotenv de lire .env **au runtime**
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
