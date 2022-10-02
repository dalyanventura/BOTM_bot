import asyncio
import nest_asyncio
import datetime
import os
from collections.abc import Iterable

import discord
import aiohttp
import builtins
from discord.ext import commands, tasks
# from discord_components import DiscordComponents
import json

from secrets import AKATOSH_BOT_TOKEN
from botm.cartes.models import Cartes
from botm.joueurs.models import Joueurs
from botm.card_owners.models import CartesJoueurs
from botm.db import session
from botm import config
# from utils.command import process_commands

nest_asyncio.apply()

def check_author(ctx):
    if ctx.author == bot.user:
        return False

    author = ctx.author
    user = session.query(Joueurs).filter(Joueurs.id_j == author.id).first()
    if user is None:
        user = Joueurs(id_j=author.id, pseudo=author.name, points=2000, pick_nb=2, Admin=False)
        session.add(user)
        session.commit()

    return True

class BOTM_Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
        # DiscordComponents(self)

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def close(self):
        await super().close()

    async def on_ready(self):
        print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
        print(f'Successfully logged in and booted...!')


# bot = BOTM_Bot()
# bot.run(AKATOSH_BOT_TOKEN)
token = os.getenv("BOTM_PEGASUS_TOKEN")
bot.run(token)