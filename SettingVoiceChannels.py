import discord  # Подключаем библиотеку
from discord.ext import commands
from timems import ms
import asyncio
import os
from datetime import datetime
import config as cf
from database import DB


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.InputText(
                label="Введите название для изменения имени канала",
                placeholder="Placeholder Test",
            ),
            *args,
            **kwargs,
        )


class MyView(discord.ui.View):
    @discord.ui.button(label="Test", row=0, style=discord.ButtonStyle.secondary)
    async def first_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="Test1", row=0, style=discord.ButtonStyle.secondary)
    async def second_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="Test2", row=0, style=discord.ButtonStyle.secondary)
    async def third_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="Test", row=0, style=discord.ButtonStyle.secondary)
    async def fourth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="Test", row=0, style=discord.ButtonStyle.secondary)
    async def fifth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="Test", row=1, style=discord.ButtonStyle.secondary)
    async def sixth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="Test", row=1, style=discord.ButtonStyle.secondary)
    async def seventh_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="Test", row=1, style=discord.ButtonStyle.secondary)
    async def eighth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="Test", row=1, style=discord.ButtonStyle.secondary)
    async def ninth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)

    @discord.ui.button(label="Test", row=1, style=discord.ButtonStyle.secondary)
    async def tenth_button_callback(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod = MyModal(title='test')
        await interaction.response.send_modal(mod)
