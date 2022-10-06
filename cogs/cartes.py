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
        args = [nom, univers, niveau, force, mana, vitesse, popularite, prix]
        cmd_args = ctx.message.content.split(" ")
        for i in range(1, len(cmd_args)):
            if args[i - 1] is None:
                args[i - 1] = cmd_args[i]
        if args[0] is None:
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
    @commands.has_role(config.ADMIN_ROLE)
    async def add(self, ctx, *, nom=None, univers=None, niveau=None, force=None, mana=None, vitesse=None, popularite=None, prix=None, image=None):
        args = [nom, univers, niveau, force, mana, vitesse, popularite, prix, image]
        cmd_args = ctx.message.content.split(" ")
        for i in range(1, len(cmd_args)):
            args[i-1] = cmd_args[i]
        if args[0] is None:
            await ctx.channel.send("Veuillez entrer un nom de carte")
            return
        if args[1] is None:
            await ctx.channel.send("Veuillez entrer un univers")
            return
        if args[2] is None:
            await ctx.channel.send("Veuillez entrer un niveau")
            return
        if args[3] is None:
            await ctx.channel.send("Veuillez entrer une force")
            return
        if args[4] is None:
            await ctx.channel.send("Veuillez entrer un mana")
            return
        if args[5] is None:
            await ctx.channel.send("Veuillez entrer une vitesse")
            return
        if args[6] is None:
            await ctx.channel.send("Veuillez entrer une popularité")
            return
        if args[7] is None:
            await ctx.channel.send("Veuillez entrer un prix")
            return
        if args[8] is None:
            await ctx.channel.send("Veuillez entrer une image")
            return
        carte = add_card(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8])
        if carte is None:
            await ctx.channel.send("Carte déjà existante")
            return
        response, file = embed_cartes(carte)
        response.set_footer(text=f"Carte ajoutée : {carte.nom} ({carte.univers})")
        await ctx.channel.send(embed=response, file=file)

    @commands.command(name="add_to_user", aliases=["add_card_to_user"])
    @commands.check(check_author)
    @commands.has_role(config.ADMIN_ROLE)
    async def add_to_user(self, ctx, *, nom=None, univers=None, niveau=None, force=None, mana=None, vitesse=None, popularite=None, user=None):
        args = [nom, univers, niveau, force, mana, vitesse, popularite, user]
        cmd_args = ctx.message.content.split(" ")
        for i in range(1, len(cmd_args)):
            args[i - 1] = cmd_args[i]
        if args[0] is None:
            await ctx.channel.send("Veuillez entrer un nom de carte")
            return
        if args[1] is None:
            await ctx.channel.send("Veuillez entrer un univers")
            return
        if args[2] is None:
            await ctx.channel.send("Veuillez entrer un niveau")
            return
        if args[3] is None:
            await ctx.channel.send("Veuillez entrer une force")
            return
        if args[4] is None:
            await ctx.channel.send("Veuillez entrer un mana")
            return
        if args[5] is None:
            await ctx.channel.send("Veuillez entrer une vitesse")
            return
        if args[6] is None:
            await ctx.channel.send("Veuillez entrer une popularité")
            return
        if args[7] is None:
            await ctx.channel.send("Veuillez entrer le pseudo d'un joueur")
            return
        print(args)
        carte = search_card(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
        if carte is None:
            await ctx.channel.send("Carte non trouvée")
            return
        user = session.query(Joueurs).filter(Joueurs.pseudo == args[7]).first()
        carte_owner = add_card_to_user(user, carte)
        response, file = embed_cartes(carte)
        response.set_footer(text=f"Carte ajoutée : {carte.nom} ({carte.univers}) pour {user.pseudo}")
        await ctx.channel.send(embed=response, file=file)

async def setup(bot):
    await bot.add_cog(CartesCog(bot))
