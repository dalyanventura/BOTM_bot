import discord
from discord.ext import commands
from sqlalchemy import func

from discord import ButtonStyle
from discord.ui import Button, View

from botm.cartes.models import Cartes
from botm.joueurs.models import Joueurs
from botm.card_owners.models import CartesJoueurs
from botm.db import session
from botm import config
from bot import check_author
from utils.command import search_card, add_card, add_card_to_user, delete_card_to_user, embed_cartes



class DeckCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deck_check", aliases=["deck_view"])
    @commands.check(check_author)
    async def deck(self, ctx):

        def _check(res):
            return res.user == ctx.author and res.channel == ctx.channel

        user = session.query(Joueurs).filter_by(id_j=ctx.author.id).first()
        deck = session.query(CartesJoueurs).filter_by(id_j=ctx.author.id).all()
        if deck is None:
            await ctx.channel.send("Vous n'avez pas de deck.")
            return
        response = discord.Embed(title=f"Deck de {user.pseudo}", color=config.COLOR)
        list_cards = []
        list_niveaux = []
        for card in deck:
            card = session.query(Cartes).filter_by(id_carte=card.id_carte).first()
            list_cards.append(card)
            list_niveaux.append(card.niveau)
        for i in range(len(list_cards)):
            for j in range(0, len(list_cards)-i-1):
                if list_niveaux[j] > list_niveaux[j+1]:
                    list_niveaux[j], list_niveaux[j+1] = list_niveaux[j+1], list_niveaux[j]
                    list_cards[j], list_cards[j+1] = list_cards[j+1], list_cards[j]
        niveau = 1
        pages = []
        field_nb = 0
        for card in list_cards:
            if card.niveau != niveau:
                pages.append(response)
                field_nb = 0
                niveau = card.niveau
                response = discord.Embed(title=f"Carte de niveau {card.niveau}", color=config.COLOR)
            if field_nb == 25:
                pages.append(response)
                field_nb = 0
                response = discord.Embed(title=f"Carte de niveau {card.niveau}", color=config.COLOR)
            response.add_field(name=f"{card.nom} ({card.univers})", value=f"Niveau {card.niveau}", inline=False)
            field_nb += 1
        pages.append(response)
        page=0

        class NextButton(Button):
            def __init__(self, page=0):
                super().__init__(label="Next", style=ButtonStyle.primary)
                self.page = page
            async def callback(self, interaction):
                if self.page == len(pages)-1:
                    await interaction.response.edit_message(embed=pages[self.page], view=None)
                else:
                    self.page += 1
                    await interaction.response.edit_message(embed=pages[self.page])

        class PrevButton(Button):
            def __init__(self, page=0):
                super().__init__(label="Previous", style=ButtonStyle.primary)
                self.page = page
            async def callback(self, interaction):
                if self.page == 0:
                    await interaction.response.edit_message(embed=pages[self.page], view=None)
                else:
                    self.page -= 1
                    await interaction.response.edit_message(embed=pages[self.page])

        class ExitButton(Button):
            def __init__(self, page=0):
                super().__init__(label="Exit", style=ButtonStyle.danger)
                self.page = page
            async def callback(self, interaction):
                await interaction.response.edit_message(embed=pages[self.page], view=None)

        button = PrevButton()
        button2 = ExitButton()
        button3 = NextButton()

        view = View()
        view.add_item(button)
        view.add_item(button2)
        view.add_item(button3)
        await ctx.send(embed=pages[0], view=view)


async def setup(bot):
    await bot.add_cog(DeckCog(bot))
