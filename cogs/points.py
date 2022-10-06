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


class PointsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="see_points", aliases=["p"])
    @commands.check(check_author)
    async def see_points(self, ctx):
        user = session.query(Joueurs).filter_by(id_j=ctx.author.id).first()
        if user is None:
            await ctx.channel.send("Vous n'avez pas de compte")
            return
        await ctx.channel.send(f"Vous avez {user.points} points")

    @commands.command(name="add_points")
    @commands.check(check_author)
    @commands.has_role(config.ADMIN_ROLE)
    async def add_points(self, ctx, *, joueur=None, points=None):
        args = [joueur, points]
        cmd = ctx.message.content.split(" ")
        print(cmd[1])
        for i in range(1, len(cmd)):
            args[i-1] = cmd[i]
        if args[0] is None:
            await ctx.channel.send("Veuillez entrer un nom de joueur")
            return
        if args[1] is None:
            await ctx.channel.send("Veuillez entrer un nombre de points")
            return
        user = session.query(Joueurs).filter_by(pseudo=args[0]).first()
        if user is None:
            await ctx.channel.send("Joueur non trouvé")
            return
        user.points += int(args[1])
        session.commit()
        await ctx.channel.send(f"{args[0]} a maintenant {user.points} points.")

    @commands.command(name="remove_points")
    @commands.check(check_author)
    @commands.has_role(config.ADMIN_ROLE)
    async def remove_points(self, ctx, *, joueur=None, points=None):
        args = [joueur, points]
        cmd = ctx.message.content.split(" ")
        for i in range(1, len(cmd)):
            args[i-1] = cmd[i]
        if args[0] is None:
            await ctx.channel.send("Veuillez entrer un nom de joueur")
            return
        if args[1] is None:
            await ctx.channel.send("Veuillez entrer un nombre de points")
            return
        user = session.query(Joueurs).filter_by(pseudo=args[0]).first()
        if user is None:
            await ctx.channel.send("Joueur non trouvé")
            return
        user.points -= int(args[1])
        session.commit()
        await ctx.channel.send(f"{args[0]} a maintenant {user.points} points.")

    @commands.command(name="set_points")
    @commands.check(check_author)
    @commands.has_role(config.ADMIN_ROLE)
    async def set_points(self, ctx, *, joueur=None, points=None):
        args = [joueur, points]
        cmd = ctx.message.content.split(" ")
        for i in range(1, len(cmd)):
            args[i-1] = cmd[i]
        if args[0] is None:
            await ctx.channel.send("Veuillez entrer un nom de joueur")
            return
        if args[1] is None:
            await ctx.channel.send("Veuillez entrer un nombre de points")
            return
        user = session.query(Joueurs).filter_by(pseudo=args[0]).first()
        if user is None:
            await ctx.channel.send("Joueur non trouvé")
            return
        user.points = int(args[1])
        session.commit()
        await ctx.channel.send(f"{args[0]} a maintenant {user.points} points.")

    @commands.command(name="top")
    @commands.check(check_author)
    async def top(self, ctx):
        users = session.query(Joueurs).order_by(Joueurs.points.desc()).all()
        embed = discord.Embed(title="Top 10", color=0x00ff00)
        for i in range(0, 10):
            embed.add_field(name=f"{i+1}. {users[i].pseudo}", value=f"{users[i].points} points", inline=False)
        await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PointsCog(bot))