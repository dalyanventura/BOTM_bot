import asyncio
import datetime
import os
from collections.abc import Iterable

import discord
import json

from secrets import AKATOSH_BOT_TOKEN
from botm.cartes.models import Cartes
from botm.joueurs.models import Joueurs
from botm.card_owners.models import CartesJoueurs
from botm.db import session
from botm import config
from utils.command import process_commands

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Le bot ne doit pas se repondre à lui meme, ce con
    if message.author == client.user:
        return

    author = message.author
    user = session.query(Joueurs).filter_by(id_j=author.id).first()
    if user is None:
        user = Joueurs(id_j=author.id, pseudo=author.name, points=2000, pick_nb=2, Admin=False)
        session.add(user)
        session.commit()

    # Si le message n'est pas une commande, on ne fait rien
    first_word = message.content.split()[0].lower()
    bot_username = client.user.name.lower()
    if not first_word.startswith('!') and not first_word.startswith(bot_username):
        return

    print(first_word)
    # Si le message est une commande, on la traite
    if first_word.startswith(bot_username) or first_word.startswith('!'):
        command = ' '.join(message.content.split()[1:])
    else:
        command = message.content[1:]

    print(command)

    # On traite la commande

    response = process_commands(session, client, message, command)
    if response is not None:
        if len(response) == 2:
            print(response[0])
            await message.channel.send(embed=response[0], file=response[1])
        elif type(response) is str:
            await message.channel.send(response)
        else:
            await message.channel.send(embed=response)

# client.run(AKATOSH_BOT_TOKEN)
client.run("BOTM_PEGASUS_TOKEN")
