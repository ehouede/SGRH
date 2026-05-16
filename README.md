# Système de Gestion des Ressources Humaines (SGRH) - Afrique de l'Ouest

Ce projet est une application web moderne de GRH adaptée aux spécificités réglementaires de l'Afrique de l'Ouest (OHADA, CNSS, IPRES).

## Architecture
- **Backend :** Django 6.0 + Django REST Framework
- **Frontend :** React + Ant Design
- **Base de données :** SQLite (Développement) / PostgreSQL (Production cible)

## Structure du Projet
- `backend/` : Code source de l'API Django.
- `frontend/` : Code source de l'application React.
- `memoire_grh.html` : Document de mémoire (en cours de rédaction).

## Installation

### Backend
1. Créer un environnement virtuel : `python -m venv venv`
2. Activer l'environnement : `.\venv\Scripts\activate`
3. Installer les dépendances : `pip install -r requirements.txt` (à générer)
4. Lancer les migrations : `python manage.py migrate`
5. Lancer le serveur : `python manage.py runserver`

### Frontend
1. Aller dans le dossier : `cd frontend`
2. Installer les dépendances : `npm install`
3. Lancer l'application : `npm run dev`

## Auteur
[Votre Nom]
