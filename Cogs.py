from discord.ext import commands
import discord
import asyncio
from timems import ms
from SettingVoiceChannels import MyView


class Configs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pin(self, ctx):
        await ctx.send('pong')

    # добавление роли пользователю
    @commands.command()
    async def giverole(self, ctx, user: discord.Member, role: discord.Role):
        await user.add_roles(role)
        await ctx.send(f"hey {ctx.author.name}, {user.name} has been giving a role called: {role.name}")

    # удаление роли у пользователя
    @commands.command()
    async def removerole(self, ctx, user: discord.Member, role: discord.Role):
        await user.remove_roles(role)
        await ctx.send(f"hey {ctx.author.name}, {user.name} has been removing a role called: {role.name}")

    # мут команда на пользовател
    @commands.command(pass_context=True)
    @commands.has_any_role(1209542003772358666, 1234801848767086644)
    async def sumute(self, ctx, member: discord.Member, time: str, prichina: str):
        emb = discord.Embed(title=f"Участник Был Замучен! Причина: {prichina}", colour=discord.Color.blue())
        await ctx.channel.purge(limit=1)

        emb.set_author(name=member.name)
        emb.set_footer(text="Его замутил {}".format(ctx.author.name))

        await ctx.send(embed=emb)
        muted_role = discord.utils.get(ctx.guild.roles, name="Mute")
        await member.add_roles(muted_role)

        # Спим X секунд, перед тем как снять роль.
        await asyncio.sleep(ms(time))
        # Снимаем роль замученного.
        await member.remove_roles(muted_role)

    # бан пользователям
    @commands.command(pass_context=True)
    @commands.has_any_role(1209542003772358666, 1234801848767086644)
    @commands.has_permissions(ban_members=True)
    async def bann(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command(name='hello', aliases=['Hi', 'Hello', 'hi'])
    async def hello(self, ctx):
        # ответ бота только на пользователя с определенной ролью
        role = discord.utils.get(ctx.guild.roles, name="Developer")
        if role in ctx.author.roles:
            await ctx.send('Hello!')
        else:
            await ctx.send('You are not a developer!')

    @commands.command()
    async def test(self, ctx: commands.Context):
        emb = discord.Embed(
            description="**Настройка канала**",
            color=discord.Color.dark_gray())
        emb.add_field(name='', value='1 -``добавить 1 слот в вашу комнату``', inline=False)
        emb.add_field(name='', value='2 -``убрать 1 слот с вашей комнаты``', inline=False)
        emb.add_field(name='', value='3 -``разрешить/Запретить вход пользователям в вашу комнату``', inline=False)
        emb.add_field(name='', value='4 -``забрать/выдать пользователю возможность говорить в вашей комнате``',
                      inline=False)
        emb.add_field(name='', value='5 -``исключить пользователя с вашей комнаты``', inline=False)
        emb.add_field(name='', value='6 -``изменить битрейт вашей комнаты``', inline=False)
        emb.add_field(name='', value='7 -``установить количество слотов в комнате``', inline=False)
        emb.add_field(name='', value='8 -``передать право владения комнатой``', inline=False)
        emb.add_field(name='', value='9 -``сменить название вашей комнаты``', inline=False)
        emb.add_field(name='', value='10 -``выдать/забрать доступ пользователю в вашу комнату``', inline=False)
        view = MyView()
        await ctx.send(embed=emb, view=view)
