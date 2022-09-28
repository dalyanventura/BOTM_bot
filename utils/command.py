import discord

from botm.cartes.models import Cartes
from botm.joueurs.models import Joueurs
from botm.card_owners.models import CartesJoueurs
from botm.db import session
from botm import config
import requests
import gdown

def process_commands(session, client, message, command):
    # On traite la commande
    response = None
    if command.startswith('help'):
        response = """```
! help : affiche ce message
! cartes <nom> : affiche la liste des cartes qui contiennent <nom>
! cartes <nom> <univers> <niveau>: affiche la carte qui contient <nom> <univers> <niveau> (Si l'univers est en deux mots, mettre un underscore)
! points : affiche le nombre de points de l'utilisateur
! pick : permet de piocher une carte
! pick <nombre> : permet de piocher <nombre> cartes
```"""
    elif command.startswith('cartes'):
        if len(command.split()) == 2:
            response = '```'
            for card in session.query(Cartes).filter(Cartes.nom.like('%' + command.split()[1] + '%')).all():
                response += f"{card.nom} ({card.univers}) Niveau: {card.niveau} Force: {card.force} Mana: {card.mana} Vitesse: {card.vitesse} Popularité: {card.popularite}\n"
            response += '```'
        elif len(command.split()) == 4:
            for card in session.query(Cartes).filter(Cartes.nom.like('%' + command.split()[1] + '%'), Cartes.univers.like('%' + command.split()[2] + '%'), Cartes.niveau == command.split()[3]).all():
                #response += f"{card.nom} ({card.univers}) Niveau: {card.niveau} Force: {card.force} Mana: {card.mana} Vitesse: {card.vitesse} Popularité: {card.popularite}\n"
                response = discord.embeds.Embed(title=f"{card.nom}")
                response.add_field(name="Univers", value=card.univers)
                response.add_field(name="Niveau", value=card.niveau)
                response.add_field(name="Force", value=card.force)
                response.add_field(name="Mana", value=card.mana)
                response.add_field(name="Vitesse", value=card.vitesse)
                response.add_field(name="Popularité", value=card.popularite)
                gdown.download(card.image, f"images/{card.nom}.gif", quiet=False)
                file = discord.File(f"images/{card.nom}.gif")
                response.set_image(url=f"attachment://{card.nom}.gif")
                return response, file
        else:
            response = '```! cartes <nom> : affiche la liste des cartes qui contiennent <nom>\n! cartes <nom> <univers> <niveau>: affiche la carte qui contient <nom> <univers> <niveau> (Si l\'univers est en deux mots, mettre un underscore)```'
    elif command.startswith('points'):
        user = session.query(Joueurs).filter_by(id_j=message.author.id).first()
        response = f"Vous avez {user.points} points."
    elif command.startswith('pick'):
        user = session.query(Joueurs).filter_by(id_j=message.author.id).first()
        if len(command.split()) == 1:
            nb = 1
        else:
            nb = int(command.split()[1])
        if nb > user.pick_nb:
            response = f"Vous ne pouvez pas piocher plus de {user.pick_nb} cartes."
        else:
            for i in range(nb):
                card = session.query(Cartes).order_by(Cartes.id_c).offset(int(session.query(Cartes).count() * random.random())).first()
                cartes_joueurs = CartesJoueurs(id_cj=card.id_c, id_j=user.id_j)
                session.add(cartes_joueurs)
                session.commit()
                response = f"Vous avez pioché la carte {card.nom}."
    else:
        response = "Commande inconnue."

    return response

