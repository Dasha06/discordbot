import discord  # Подключаем библиотеку
from timems import ms
import asyncio
import os
from datetime import datetime
import config as cf
from database import DB
from myBot import MyBot

# пока не работает через отдельный файл, разобраться


class ChangeName(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        intents = discord.Intents.default()  # Подключаем "Разрешения"
        intents.message_content = True
        intents.members = True
        # Задаём префикс и интенты
        self.bot = MyBot(command_prefix='/', intents=intents)
        self.database = DB()
        self.connection = self.database.create_connection("urVChan.sqlite")
        super().__init__(
            discord.ui.InputText(
                label="Введите название для изменения имени канала",
                placeholder="Placeholder Test",
            ),
            *args,
            **kwargs,
        )

    async def callback(self, interaction: discord.Interaction):
        nam = self.children[0].value
        chanid = self.database.find_users_vchan(self.connection, interaction.user.id)
        vchan = self.bot.get_channel(chanid)
        await vchan.edit(name=nam)
        await interaction.response.send_message("Название успешно изменено")


class MyView(discord.ui.View):
    @discord.ui.button(label="1", row=0, style=discord.ButtonStyle.secondary)
    async def first_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='1')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="2", row=0, style=discord.ButtonStyle.secondary)
    async def second_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="3", row=0, style=discord.ButtonStyle.secondary)
    async def third_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="4", row=0, style=discord.ButtonStyle.secondary)
    async def fourth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="5", row=0, style=discord.ButtonStyle.secondary)
    async def fifth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="6", row=1, style=discord.ButtonStyle.secondary)
    async def sixth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="7", row=1, style=discord.ButtonStyle.secondary)
    async def seventh_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="8", row=1, style=discord.ButtonStyle.secondary)
    async def eighth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="9", row=1, style=discord.ButtonStyle.secondary)
    async def ninth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = ChangeName(title='Изменить название приватного канала')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="10", row=1, style=discord.ButtonStyle.secondary)
    async def tenth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)
