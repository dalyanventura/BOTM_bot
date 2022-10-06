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
    async def pick(self, ctx):
        nom = ctx.message.content.split(" ")[1]
        niveau = ctx.message.content.split(" ")[2]

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
        if user.pick_nb == 0:
            await ctx.channel.send("Vous n'avez plus de picks")
            return
        card = search_card(nom=nom, niveau=niveau)
        if card is None:
            await ctx.channel.send("Carte non trouvée")
            return
        card_found = delete_card_to_user(user.id_j, card.id_carte)
        if card_found is None:
            await ctx.channel.send("Vous n'avez pas cette carte dans votre deck.")
            return
        user.pick_nb -= 1
        new_card = session.query(Cartes).filter_by(niveau=niveau).order_by(func.random()).first()
        add_card_to_user(user, new_card)
        response, file = embed_cartes(new_card)
        response.set_footer(text=f"Carte remplacée : {card.nom} ({card.univers}) pour {user.pseudo}")
        session.commit()
        await ctx.channel.send(embed=response, file=file)

    @commands.command(name="pick_nb", aliases=["pick_number"])
    @commands.check(check_author)
    async def pick_nb(self, ctx):
        user = session.query(Joueurs).filter_by(id_j=ctx.author.id).first()
        if user is None:
            await ctx.channel.send("Vous n'avez pas de compte")
            return
        await ctx.channel.send(f"Vous avez {user.pick_nb} picks")

    @commands.command(name="add_pick", aliases=["add_pick_nb"])
    @commands.check(check_author)
    @commands.has_role(config.ADMIN_ROLE)
    async def add_pick(self, ctx, *, user_pseudo):
        user = session.query(Joueurs).filter_by(pseudo=user_pseudo).first()
        if user is None:
            await ctx.channel.send("Utilisateur non trouvé")
            return
        user.pick_nb += 1
        session.commit()
        await ctx.channel.send(f"Vous avez maintenant {user.pick_nb} picks")

    @commands.command(name="remove_pick", aliases=["remove_pick_nb"])
    @commands.check(check_author)
    @commands.has_role(config.ADMIN_ROLE)
    async def remove_pick(self, ctx, *, user_pseudo):
        user = session.query(Joueurs).filter_by(pseudo=user_pseudo).first()
        if user is None:
            await ctx.channel.send("Utilisateur non trouvé")
            return
        user.pick_nb -= 1
        session.commit()
        await ctx.channel.send(f"Vous avez maintenant {user.pick_nb} picks")



async def setup(bot):
    await bot.add_cog(PickCog(bot))
