# Dockerfile

# Utiliser une image Python légère
FROM python:3.13-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers du projet
COPY . /app/

# Exposer le port interne sur lequel Gunicorn écoutera
EXPOSE 8000

# Commande pour lancer Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "eduathena_backend.wsgi:application", "--workers=3"]
