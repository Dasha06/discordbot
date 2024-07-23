import discord
from discord.ext import commands


class MyBot(commands.Bot): # subclass discord.Bot
    def __init__(self, *args, **kwargs) -> None:
        # Forward all arguments, and keyword-only arguments to commands.Bot
        super().__init__(*args, **kwargs)

    async def on_ready(self): # override on_ready
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')