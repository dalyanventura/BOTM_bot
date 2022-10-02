import discord
from discord.ext import commands
from sqlalchemy import func

from botm.cartes.models import Cartes
from botm.joueurs.models import Joueurs
from botm.card_owners.models import CartesJoueurs
from botm.db import session
from botm import config
from bot import check_author
from utils.command import search_card, add_card, add_card_to_user, embed_cartes


class CartesCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="carte", aliases=["card"])
    @commands.check(check_author)
    async def carte(self, ctx, *, nom=None, univers=None, niveau=None, force=None, mana=None, vitesse=None, popularite=None, prix=None):
        if nom is None:
            await ctx.channel.send("Veuillez entrer un nom de carte")
            return
        card = search_card(nom, univers, niveau, force, mana, vitesse, popularite, prix)
        if card is None:
            await ctx.channel.send("Carte non trouvée")
            return
        response, file = embed_cartes(card)
        await ctx.channel.send(embed=response, file=file)

    @commands.command(name="carte_random", aliases=["card_random"])
    @commands.check(check_author)
    async def carte_random(self, ctx):
        card = session.query(Cartes).order_by(func.random()).first()
        response, file = embed_cartes(card)
        await ctx.channel.send(embed=response, file=file)

    @commands.command(name="add", aliases=["add_card"])
    @commands.check(check_author)
    async def add(self, ctx, *, nom=None, univers=None, niveau=None, force=None, mana=None, vitesse=None, popularite=None, prix=None, image=None):
        if nom is None:
            await ctx.channel.send("Veuillez entrer un nom de carte")
            return
        if univers is None:
            await ctx.channel.send("Veuillez entrer un univers")
            return
        if niveau is None:
            await ctx.channel.send("Veuillez entrer un niveau")
            return
        if force is None:
            await ctx.channel.send("Veuillez entrer une force")
            return
        if mana is None:
            await ctx.channel.send("Veuillez entrer un mana")
            return
        if vitesse is None:
            await ctx.channel.send("Veuillez entrer une vitesse")
            return
        if popularite is None:
            await ctx.channel.send("Veuillez entrer une popularité")
            return
        if prix is None:
            await ctx.channel.send("Veuillez entrer un prix")
            return
        if image is None:
            await ctx.channel.send("Veuillez entrer une image")
            return
        carte = add_card(nom, univers, niveau, force, mana, vitesse, popularite, prix, image)
        if carte is None:
            await ctx.channel.send("Carte déjà existante")
            return
        response, file = embed_cartes(carte)
        response.set_footer(text=f"Carte ajoutée : {carte.nom} ({carte.univers})")
        await ctx.channel.send(embed=response, file=file)

    @commands.command(name="add_to_user", aliases=["add_card_to_user"])
    @commands.check(check_author)

    async def add_to_user(self, ctx, *, nom=None, univers=None, niveau=None, force=None, mana=None, vitesse=None, popularite=None, prix=None, image=None, user=None):
        if nom is None:
            await ctx.channel.send("Veuillez entrer un nom de carte")
            return
        if univers is None:
            await ctx.channel.send("Veuillez entrer un univers")
            return
        if niveau is None:
            await ctx.channel.send("Veuillez entrer un niveau")
            return
        if force is None:
            await ctx.channel.send("Veuillez entrer une force")
            return
        if mana is None:
            await ctx.channel.send("Veuillez entrer un mana")
            return
        if vitesse is None:
            await ctx.channel.send("Veuillez entrer une vitesse")
            return
        if popularite is None:
            await ctx.channel.send("Veuillez entrer une popularité")
            return
        if prix is None:
            await ctx.channel.send("Veuillez entrer un prix")
            return
        if image is None:
            await ctx.channel.send("Veuillez entrer une image")
            return
        if user is None:
            await ctx.channel.send("Veuillez entrer un utilisateur")
            return
        carte = search_card(nom, univers, niveau, force, mana, vitesse, popularite, prix)
        carte_owner = add_card_to_user(nom, univers, niveau, force, mana, vitesse, popularite, prix, image, user)
        response, file = embed_cartes(carte)
        response.set_footer(text=f"Carte ajoutée : {carte.nom} ({carte.univers}) pour {user.pseudo}")
        await ctx.channel.send("Carte ajoutée à l'utilisateur")

async def setup(bot):
    await bot.add_cog(CartesCog(bot))
