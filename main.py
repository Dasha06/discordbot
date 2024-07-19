import discord  # Подключаем библиотеку
from discord.ext import commands
from timems import ms
import asyncio
import os
from datetime import datetime
import config as cf
from database import DB
from SettingVoiceChannels import MyView

intents = discord.Intents.default()  # Подключаем "Разрешения"
intents.message_content = True
intents.members = True
# Задаём префикс и интенты
bot = commands.Bot(command_prefix='/', intents=intents)
vChannels = DB()
connection = vChannels.create_connection("urVChan.sqlite")
client = discord.Client(intents=intents)

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

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Your Modal Results",
            fields=[
                discord.EmbedField(
                    name="First Input", value=self.children[0].value, inline=False
                ),
            ],
            color=discord.Color.random(),
        )
        await interaction.response.send_message(embeds=[embed])


@client.event
async def on_message(message):
    if message.author == bot.user:
        return


@bot.event
async def on_member_update(before, after):
    # Логи по тому, какие роли были изменены у данного пользователя
    if before.roles != after.roles:
        async for event in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
            if getattr(event.target, "id", None) != before.id:
                continue
            break
        channel = discord.utils.get(before.guild.channels, name="log") #ID канала с логами, а именно куда должны появлятся сообщения об изменениях ролях.
        emb = discord.Embed(description=f'**{event.user.mention}\n Обновил роли {before.mention}**', colour=discord.Color.orange())
        emb.add_field(name='Роли до', value=" ".join([r.mention for r in before.roles][1:]), inline=False)
        emb.add_field(name='Роли после', value=" ".join([r.mention for r in after.roles][1:]), inline=False)
        changed_roles = []
        for role in before.roles:
            if role in after.roles:
                pass
            else:
                changed_roles.append(role)

        for role in after.roles:
            if role in before.roles:
                pass
            else:
                if role in changed_roles:
                    pass
                else:
                    changed_roles.append(role)

        text = ""
        for role in changed_roles:
            text = text + role.mention + " "
        emb.add_field(name="Изменённые роли", value=text, inline=False)

        await channel.send(embed=emb)


@bot.event
async def on_message_edit(before, after):
    if not after.author.bot:
        channel = discord.utils.get(before.guild.channels, name="log")
        embed = discord.Embed(description=f"**{after.author.mention} \n Канал: {after.channel.mention} \n Отредактировал сообщение {after.jump_url}**",
                              color=discord.Color.blue())
        embed.add_field(name="До", value=before.content, inline=False)
        embed.add_field(name="После", value=after.content, inline=False)
        await channel.send(embed=embed)


@bot.event
async def on_message_delete(message):
    if not message.author.bot:
        channel = discord.utils.get(message.guild.channels, name="log")
        embed = discord.Embed(description=f"**{message.author.mention} \n Канал: {message.channel.mention} \n Удалил сообщение**", color=discord.Color.red())
        embed.add_field(name="Содержание", value=message.content, inline=False)
        await channel.send(embed=embed)

# создание своего приват канала через канал start
@bot.event
async def on_voice_state_update(member, before, after):
    global category
    GUILD = bot.get_guild(1209541686821261342)
    if after.channel is not None:
        if after.channel.id == 1240184145947263016:
            category = discord.utils.get(GUILD.categories, name='секретка')
            if discord.utils.get(GUILD.channels, name=f'Приват-{member.display_name}') != None:
                await member.move_to(discord.utils.get(GUILD.channels, name=f'Приват-{member.display_name}')    )
                return
            # overwrite = {
            #     GUILD.default_role: discord.PermissionOverwrite(read_messages=False, manage_channels=False),
            #     member: discord.PermissionOverwrite(connect=True, speak=True, view_channel=True, stream=True, manage_channels=True,
            #                                         kick_members=True, mute_members=True, priority_speaker=True)}

            v_channel = await GUILD.create_voice_channel(name=f'Приват-{member.display_name}', category=category)
            t_channel = await GUILD.create_text_channel(name=f'Выдача прав ({member.display_name})', category=category)
            vChannels.add_channel(connection, v_channel.id, t_channel.id)
            await member.move_to(v_channel)

        if before.channel is not None:
            if len(before.channel.members) == 0 and before.channel.id != 1240184145947263016 and before.channel in category.voice_channels:
                await before.channel.delete()
                vChannels.delete_Channel(connection, before.channel.id)

    elif before.channel is not None and before.channel.id in vChannels.find_vchannel(connection):
        if len(before.channel.members) == 0:
            await before.channel.delete()
            vChannels.delete_Channel(connection, before.channel.id)
    # elif len(before.channel.members) == 0:
    #     await before.channel.delete()
    #     vChannels.delete_Channel(connection, before.channel.id)

    # if before.channel is not None:
    #     channels = private.find_one({'_id':member.id})
    #     t_channel = bot.get_channel(channels['text_id'])
    #     v_channel = bot.get_channel(channels['voice_id'])
    #     if before.channel.id != v_channel.id:
    #         return
    #     await t_channel.send(f'`[PRIVATE]`: {member.mention}, Your private will be deleted in 1 minute!')
    #     await asyncio.sleep(60000)
    #     await t_channel.delete()
    #     await v_channel.delete()
    #     roles.delete_one({'_id': member.id})


@bot.command(name='hello', aliases=['Hi', 'Hello', 'hi'])
async def hello(ctx):
    # ответ бота только на пользователя с определенной ролью
    role = discord.utils.get(ctx.guild.roles, name="Developer")
    if role in ctx.author.roles:
        await ctx.send('Hello!')
    else:
        await ctx.send('You are not a developer!')


@bot.command()
async def pin(ctx):
    await ctx.send('pong')


# добавление роли пользователю
@bot.command()
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"hey {ctx.author.name}, {user.name} has been giving a role called: {role.name}")


# удаление роли у пользователя
@bot.command()
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"hey {ctx.author.name}, {user.name} has been removing a role called: {role.name}")


# мут команда на пользователя
@bot.command(pass_context=True)
@commands.has_any_role(1209542003772358666, 1234801848767086644)
async def sumute(ctx, member: discord.Member, time: str, prichina: str):
    emb = discord.Embed(title=f"Участник Был Замучен! Причина: {prichina}", colour=discord.Color.blue())
    await ctx.channel.purge(limit=1)

    emb.set_author(name=member.name)
    emb.set_footer(text="Его замутил {}".format(ctx.author.name))
    channel = bot.get_channel(int(1228357921952497746))

    await ctx.send(embed=emb)
    muted_role = discord.utils.get(ctx.guild.roles, name="Mute")
    await member.add_roles(muted_role)

    # Спим X секунд, перед тем как снять роль.
    await asyncio.sleep(ms(time))
    # Снимаем роль замученного.
    await member.remove_roles(muted_role)


# бан пользователям
@bot.command(pass_context=True)
@commands.has_any_role(1209542003772358666, 1234801848767086644)
@commands.has_permissions(ban_members=True)
async def bann(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


@bot.command()
async def test(ctx: commands.Context):

    view = MyView()
    await ctx.send('', view=view)


# изменение название голосового канала
@bot.command()
async def changevc(ctx, name: str, changed: str):
    vc = discord.utils.get(ctx.guild.channels, name=name)
    await vc.edit(name=changed)
    await ctx.send(f"{name} изменил имя на {changed}")


# @bot.command()
# async def createvc(ctx, *name: str):
#     guild = bot.get_guild(1209541686821261342)
#     member = bot.get_user(ctx.author.id)
#     c = discord.utils.get(ctx.guild.categories, id=1228334654759768165)
#
#     overwrites = {
#         guild.default_role: discord.PermissionOverwrite(),
#         member: discord.PermissionOverwrite(connect=True)}
#     v_channel = await guild.create_voice_channel(name=f"Канал-{name}", category=c, overwrites=overwrites)


bot.run(cf.TOKEN)
