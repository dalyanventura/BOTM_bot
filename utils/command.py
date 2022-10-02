import discord
from sqlalchemy import func

from botm.cartes.models import Cartes
from botm.joueurs.models import Joueurs
from botm.card_owners.models import CartesJoueurs
from botm.db import session
from botm import config
import requests
import gdown

def search_card(nom=None, univers=None, niveau=None, force=None, mana=None, vitesse=None, popularite=None, prix=None):
    if nom is not None:
        query = session.query(Cartes).filter(Cartes.nom.like('%' + nom + '%'))
    if univers is not None:
        query = query.filter(Cartes.univers.like('%' + univers + '%'))
    if niveau is not None:
        query = query.filter(Cartes.niveau == niveau)
    if force is not None:
        query = query.filter(Cartes.force == force)
    if mana is not None:
        query = query.filter(Cartes.mana == mana)
    if vitesse is not None:
        query = query.filter(Cartes.vitesse == vitesse)
    if popularite is not None:
        query = query.filter(Cartes.popularite == popularite)
    if prix is not None:
        query = query.filter(Cartes.prix == prix)
    return query.first()

def add_card(nom, univers, niveau, force, mana, vitesse, popularite, image, prix):
    delete_char = "_"
    nom = nom.replace(delete_char, " ")
    univers = univers.replace(delete_char, " ")
    id_carte = session.query(func.max(Cartes.id_carte)).scalar() + 1
    print(id_carte)
    card = Cartes(id_carte, nom, univers, int(niveau), int(force), int(mana), int(vitesse), int(popularite), int(prix), image)
    session.add(card)
    session.commit()
    return card

def add_card_to_user(user, card):
    try:
        card_owner = CartesJoueurs(id_j=user.id_j, id_carte=card.id_carte, nb_cartes=1)
        session.add(card_owner)
        session.commit()
        return card_owner
    except Exception as e:
        session.query(CartesJoueurs).filter_by(id_j=user.id_j, id_carte=card.id_carte).update({CartesJoueurs.nb_cartes: CartesJoueurs.nb_cartes + 1})
        session.commit()
        return session.query(CartesJoueurs).filter_by(id_j=user.id_j, id_carte=card.id_carte).first()

def delete_card_to_user(id_user, id_carte):
    session.query(CartesJoueurs).filter_by(id_j=id_user, id_carte=id_carte).update({CartesJoueurs.nb_cartes: CartesJoueurs.nb_cartes - 1})
    session.commit()
    try:
        if session.query(CartesJoueurs).filter_by(id_j=id_user, id_carte=id_carte).first().nb_cartes == 0:
            session.query(CartesJoueurs).filter_by(id_j=id_user, id_carte=id_carte).delete()
            session.commit()
        return True
    except Exception as e:
        return False

def embed_cartes(card):
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

# async def process_commands(session, client, message, command):
#     # On traite la commande
#     response = None
#     file = None
#     if command.startswith('help'):
#         response = """```
# ! help : affiche ce message
# ! cartes <nom> : affiche la liste des cartes qui contiennent <nom>
# ! cartes <nom> <univers> <niveau> <force> <mana> <vitesse> <popularite> : affiche la carte qui contient <nom> <univers> <niveau> <force> <popularite> (Si une des caractérisiques est en deux mots, mettre un underscore)
# ! cartes random : affiche une carte au hasard
# ! points : affiche le nombre de points de l'utilisateur
# ! add <nom> <univers> <niveau> <force> <mana> <vitesse> <popularite> <image> <prix>: ajoute une carte dans la base de données
# ! add joueur <nom> <univers> <niveau> <force> <mana> <vitesse> <popularite> <pseudo> : ajoute une carte dans la base de données pour un joueur
# ! see deck <pseudo> : affiche le deck du joueur
# ! pick <nom> <niveau> : remplace une carte dans le deck du joueur par une carte de la base de données du même niveau
# ```"""
#     elif command.startswith('cartes'):
#         args = command.split(' ')
#         if args[1] == 'random':
#             card = session.query(Cartes).order_by(func.random()).first()
#             response, file = embed_cartes(card)
#         elif len(args) >= 2:
#             if len(args) < 8:
#                 while len(args) < 8:
#                     args.append(None)
#             card = search_card(nom=args[1], univers=args[2], niveau=args[3], force=args[4], mana=args[5], vitesse=args[6], popularite=args[7])
#             print(card)
#             if card is None:
#                 response = "Aucune carte trouvée"
#             else:
#                 response, file = embed_cartes(card)
#         else:
#             response = '```! cartes <nom> : affiche la liste des cartes qui contiennent <nom>\n! cartes <nom> <univers> <niveau> <force> <mana> <vitesse> <popularite> : affiche la carte qui contient <nom> <univers> <niveau> <force> <mana> <vitesse> <popularite> (Si une des caractéristiques est en deux mots, mettre un underscore)```'
#     elif command.startswith('points'):
#         user = session.query(Joueurs).filter_by(id_j=message.author.id).first()
#         response = f"Vous avez {user.points} points."
#     elif command.startswith('add'):
#         args = command.split(' ')
#         if len(args) == 10 and args[1] != 'joueur':
#             card = add_card(args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9])
#             response, file = embed_cartes(card)
#             response.set_footer(text=f"Carte ajoutée : {card.nom} ({card.univers})")
#         elif len(args) == 10 and args[1] == 'joueur':
#             user = session.query(Joueurs).filter_by(pseudo=args[9]).first()
#             card = search_card(nom=args[2], univers=args[3], niveau=args[4], force=args[5], mana=args[6], vitesse=args[7], popularite=args[8])
#             card_owner = add_card_to_user(user, card)
#             response, file = embed_cartes(card)
#             response.set_footer(text=f"Carte ajoutée : {card.nom} ({card.univers}) pour {user.pseudo}")
#         else:
#             response = '```! add <nom> <univers> <niveau> <force> <mana> <vitesse> <popularite> <image> <prix> : ajoute une carte dans la base de données\n! add joueur <nom> <univers> <niveau> <force> <mana> <vitesse> <popularite> <pseudo> : ajoute une carte dans la base de données pour un joueur```'
#     elif command.startswith('see deck'):
#         args = command.split(' ')
#         if len(args) == 3:
#             user = session.query(Joueurs).filter_by(pseudo=args[2]).first()
#             cards_owner = session.query(CartesJoueurs).filter_by(id_j=user.id_j).all()
#             response = discord.embeds.Embed(title=f"Deck de {user.pseudo}")
#             list_cards = []
#             list_niveau = []
#             for card_own in cards_owner:
#                 card = session.query(Cartes).filter_by(id_carte=card_own.id_carte).first()
#                 list_cards.append(card)
#                 list_niveau.append(card.niveau)
#             for i in range(len(list_cards)):
#                 for j in range(0, len(list_cards)-i-1):
#                     if list_niveau[j] > list_niveau[j+1]:
#                         list_niveau[j], list_niveau[j+1] = list_niveau[j+1], list_niveau[j]
#                         list_cards[j], list_cards[j+1] = list_cards[j+1], list_cards[j]
#             niveau = 1
#             pages = []
#             field_nb = 0
#             for card in list_cards:
#                 if card.niveau != niveau:
#                     pages.append(response)
#                     response=discord.embeds.Embed(title=f"Carte de niveau {card.niveau}*")
#                     niveau = card.niveau
#                 if field_nb > 24:
#                     pages.append(response)
#                     response = discord.embeds.Embed(title=f"Carte de niveau {card.niveau}*")
#                     field_nb = 0
#                 response.add_field(name=f"{card.nom} Lvl ({card.niveau})* - {card.univers}", value=f"Force : {card.force} - Mana : {card.mana} - Vitesse : {card.vitesse} - Popularité : {card.popularite}")
#                 field_nb += 1
#             pages.append(response)
#
#             await message.channel.send(embed=pages[0], components=[Button(style=ButtonStyle.blue, label="Page suivante", custom_id="next_page"), Button(style=ButtonStyle.blue, label="Page précédente", custom_id="previous_page")])
#             page = 0
#             while True:
#                 interaction = await client.wait_for("button_click")
#                 if interaction.component.custom_id == "next_page":
#                     print("next")
#                     page += 1
#                     if page > len(pages):
#                         page = 0
#                     await interaction.send(embed=pages[page])
#                 elif interaction.component.custom_id == "previous_page":
#                     print("previous")
#                     page -= 1
#                     if page < 0:
#                         page = len(pages)
#                     await interaction.send(embed=pages[page])
#         else:
#             response = '```! see deck <pseudo> : affiche le deck du joueur```'
#     elif command.startswith('pick'):
#         args = command.split(' ')
#         if len(args) == 3:
#             user = session.query(Joueurs).filter_by(id_j=message.author.id).first()
#             if user.pick_nb > 0:
#                 card = search_card(nom=args[1], niveau=args[2])
#                 if card is not None:
#                     card_found = delete_card_to_user(user.id_j, card.id_carte)
#                     if card_found:
#                         card = session.query(Cartes).filter_by(niveau=args[2]).order_by(func.random()).first()
#                         card_owner = add_card_to_user(user, card)
#                         user.pick_nb -= 1
#                         response, file = embed_cartes(card)
#                         response.set_footer(text=f"Carte ajoutée : {card.nom} ({card.univers}) pour {user.pseudo}")
#                     else:
#                         response = "Vous n'avez pas cette carte dans votre deck."
#                 else:
#                     response = "Aucune carte trouvée."
#             else:
#                 response = "Vous n'avez plus de pick."
#         else:
#             response = '```! pick <nom> <niveau> : remplace une carte dans le deck du joueur par une carte de la base de données du même niveau```'
#     else:
#         response = "Commande inconnue."
#
#     return response, file
#
