# Utilisez une image de base officielle de Python 3.11
FROM python:3.11-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail dans le conteneur
WORKDIR /code

# Installer TensorFlow et afficher sa version
RUN pip install --no-cache-dir tensorflow && \
    python -c "import tensorflow as tf; print('TensorFlow version :', tf.__version__)"

# Installer les bibliothèques nécessaires
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Installer les dépendances
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code dans le répertoire de travail
COPY . /code/

# Commande pour démarrer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
