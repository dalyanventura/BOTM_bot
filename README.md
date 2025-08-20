# Bot pour le jeu de cartes *Battle of the Multiverse* (BOTM)

Ce bot est un outil pour jouer à BOTM en ligne. Il permet de créer des nouveaux joueurs, de nouveaux decks, et jouer aux
différents duels et jeux au sein du serveur Discord. Il est possible de jouer à plusieurs sur un même serveur Discord.

## Installation et setup

### Prérequis

Vous devez avoir installé au préalable Python sur votre machine. Vous pouvez le télécharger [ici](https://www.python.org/downloads/).
Vous devez aussi avoir un interpréteur Python 3.6 ou supérieur. Vous pouvez vérifier votre version avec la commande `python --version`.

### Installation des dépendances

```python
# Il est possible d'installer un environnement virtuel avant d'installer les dépendances
python -m venv env
source env/bin/activate
# Installation des dépendances
pip install -r requirements.txt
```

### Lancement du bot

```python
# Lancement du bot
python bot.py
```

## Utilisation sur Heroku

Le bot est installé sur Heroku. Il est possible de le lancer sur Heroku en suivant les étapes suivantes :

1. Créer un compte sur Heroku
2. Créer une nouvelle application
3. Se rendre dans l'onglet "Deploy" et lier le dépôt Github
4. Se rendre dans l'onglet "Resources" et activer le worker

### Commandes pour maintenir le projet Heroku

```python
# Pour voir les logs
heroku logs --tail --app <nom de l'application>
# Pour redémarrer le worker
heroku ps:restart worker --app <nom de l'application>
# Pour mettre à jour la base de données
heroku pg:push <nom de la base de données locale> DATABASE_URL --app <nom de l'application>
```
