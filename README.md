# Développez une application Web en utilisant Django

Developper une application web permettant à une communauté d'utilisateurs
de consulterou de solliciter une critique de livres à la demande

## Installation

1. # Clonez le dépôt:

   `git clone https://github.com/Saurelien/project_9.git`
3. # Accédez au répertoire du projet :
   Utilisez la commande cd pour accéder au répertoire du projet que vous venez de cloner :
   cd nom_du_projet
3. # Créez et activez un environnement virtuel (facultatif mais recommandé):
   `python -m venv venv`
5. # Activez ensuite l'environnement virtuel :
   Sur Windows :
   `venv\Scripts\activate`
   Sur macOS et Linux :
   `source venv/bin/activate`
3. # Installez les dépendances.
   Si le projet a des dépendances listées dans un fichier requirements.txt, installez-les en utilisant la commande suivante
   ` pip install -r requirements.txt `

4. # Fonctionnalités

- ## Ce projet permet:
- ### En tant qu'invité de s'inscire et se connecter
- ### S'abonner aux utilisateur ou se désabonner
- ### Afficher les utilisateurs suivis et abonnés
- ### Créer un ticket pour demander des avis sur un Livre\ Article
- ### De créer des critiques en réponse à un ticket d'un utilisateur suivi
- ### De créer une critique pour un ticket 
- ### D'avoir accès au panel administrateur " Si l'utilisateur est un super user "
- ### Se deconnecter

5. # Exécutez le projet 
6. ## en utilisant la commande `python manage.py runserver`.
7. ## Cela devrait démarrer le serveur de developpement local: http://127.0.0.1:8000/
