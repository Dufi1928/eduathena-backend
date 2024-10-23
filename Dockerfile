# Utiliser une image de base Python 3.13
FROM python:3.13-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip à la dernière version
RUN pip install --upgrade pip

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers du projet
COPY . .

# Exposer le port (ajustez si nécessaire)
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["gunicorn", "votre_projet.wsgi:application", "--bind", "0.0.0.0:8000"]
