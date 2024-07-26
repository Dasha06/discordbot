import discord  # Подключаем библиотеку
from discord.ext import commands
from timems import ms
import asyncio
import os
from datetime import datetime
import config as cf
from database import DB
from Cogs import Configs
from myBot import MyBot

intents = discord.Intents.default()  # Подключаем "Разрешения"
intents.message_content = True
intents.members = True
# Задаём префикс и интенты
bot = MyBot(command_prefix='/', intents=intents)
vChannels = DB()
connection = vChannels.create_connection("urVChan.sqlite")
client = discord.Client(intents=intents)


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

            v_channel = await GUILD.create_voice_channel(name=f'Приват-{member.display_name}', category=category)
            vChannels.add_channel(connection, v_channel.id, member.id)
            await member.move_to(v_channel)

        if before.channel is not None:
            if len(before.channel.members) == 0 and before.channel.id != 1240184145947263016 and before.channel in category.voice_channels:
                await before.channel.delete()
                vChannels.delete_Channel(connection, before.channel.id)

    elif before.channel is not None and before.channel.id in vChannels.find_vchannel(connection):
        if len(before.channel.members) == 0:
            await before.channel.delete()
            vChannels.delete_Channel(connection, before.channel.id)


bot.add_cog(Configs(bot))


bot.run(cf.TOKEN)
