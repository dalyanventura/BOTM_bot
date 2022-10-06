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


class Boutique(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="achat", aliases=["achat_carte"])
    @commands.check(check_author)
    async def achat(self, ctx, *, nom=None, univers=None, niveau=None, force=None, mana=None, vitesse=None, popularite=None):
        args = [nom, univers, niveau, force, mana, vitesse, popularite]
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
        card = search_card(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
        if card is None:
            await ctx.channel.send("Carte non trouvée")
            return
        user = session.query(Joueurs).filter(Joueurs.id_j == ctx.author.id).first()
        if user is None:
            await ctx.channel.send("Vous n'avez pas de compte")
            return
        if user.points < card.prix:
            await ctx.channel.send("Vous n'avez pas assez de points")
            return
        card_owner = add_card_to_user(user, card)
        card = session.query(Cartes).filter(Cartes.id_carte == card_owner.id_carte).first()
        user.points -= card.prix
        session.commit()
        response, file = embed_cartes(card)
        response.set_footer(text=f"Carte ajoutée. Vous avez maintenant {user.points} points.")
        await ctx.channel.send(embed=response, file=file)


async def setup(bot):
    await bot.add_cog(Boutique(bot))