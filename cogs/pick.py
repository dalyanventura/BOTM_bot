import discord
from discord.ext import commands
from sqlalchemy import func

from botm.cartes.models import Cartes
from botm.joueurs.models import Joueurs
from botm.card_owners.models import CartesJoueurs
from botm.db import session
from bot import check_author
from utils.command import search_card, add_card, add_card_to_user, delete_card_to_user, embed_cartes
from botm import config

class PickCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pick", aliases=["pick_card"])
    async def pick(self, ctx, *, nom=None, niveau=None):
        if nom is None:
            await ctx.channel.send("Veuillez entrer un nom de carte")
            return
        if niveau is None:
            await ctx.channel.send("Veuillez entrer un niveau")
            return
        user = session.query(Joueurs).filter_by(id_j=ctx.author.id).first()
        if user is None:
            await ctx.channel.send("Vous n'avez pas de compte")
            return
        if user.picks == 0:
            await ctx.channel.send("Vous n'avez plus de picks")
            return
        card = search_card(nom=nom, niveau=niveau)
        if card is None:
            await ctx.channel.send("Carte non trouvée")
            return
        card_found = delete_card_to_user(user.id_j, card)
        if card_found is None:
            await ctx.channel.send("Vous n'avez pas cette carte dans votre deck.")
            return
        user.pick -= 1
        response, file = embed_cartes(card)
        response.set_footer(text=f"Carte ajoutée : {card.nom} ({card.univers}) pour {user.pseudo}")
        await ctx.channel.send(embed=response, file=file)

async def setup(bot):
    await bot.add_cog(PickCog(bot))

