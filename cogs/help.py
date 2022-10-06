import discord
from discord.ext import commands
from sqlalchemy import func

from botm.cartes.models import Cartes
from botm.joueurs.models import Joueurs
from botm.card_owners.models import CartesJoueurs
from botm.db import session
from botm import config
from bot import check_author
import requests
import gdown

class HelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        print("Help cog loaded")

    @commands.command()
    @commands.check(check_author)
    async def help_cmd(self, ctx):
        response = discord.embeds.Embed(title="Commandes disponibles")
        response.add_field(name="!help", value="Affiche les commandes disponibles")
        response.add_field(name="!carte", value="Affiche les informations d'une carte. (nom, niveau, univers, force, mana, vitesse, popularite, prix)")
        response.add_field(name="!carte_random", value="Affiche une carte aléatoire")
        response.add_field(name="!add", value="Ajoute une carte dans la base de donnée (nom, univers, niveau, force, mana, vitesse, popularite, prix, image)")
        response.add_field(name="!add_joueur", value="Ajoute une carte dans le deck d'un joueur. (nom, univers, niveau, force, mana, vitesse, popularite, joueur)")
        response.add_field(name="!deck", value="Affiche votre deck")
        response.add_field(name="!pick", value="Retire une carte de votre deck et remplacez la par une carte de même niveau")
        response.add_field(name="!points", value="Affiche vos points")
        await ctx.channel.send(embed=response)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
