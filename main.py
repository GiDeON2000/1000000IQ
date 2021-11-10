import nextcord
from nextcord.ext import commands

import config
from config import settings
from config import colors

import os
import json
import logging

from Utils import functions

#====================================================

intents = nextcord.Intents.all()

logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(levelname)s %(message)s",
                    datefmt="%m/%d/%y - %H:%M:%S %Z")

def_prefix = settings['DEF_PREFIX']
token = settings['TOKEN']

client = commands.Bot(command_prefix=functions.get_prefix, intents=intents)
client.remove_command('help')

ConnectionMain = False

#====================================================

@client.event
async def on_ready():
    global ConnectionMain

    if not ConnectionMain:
        print("\n======================")
        print("Connected to Discord\n")
        print(f"Bot tag: {client.user.name}#{client.user.discriminator}")
        print(f"ID: {str(client.user.id)}")
        print("======================\n")

        ConnectionMain = True

    else:
        print("\n======================")
        print("ERROR: The on_ready bot event worked again!")
        print("======================\n")



@client.event
async def on_disconnect():
    print("\n======================")
    print("ERROR: The bot has disconnected from Discord!")
    print("======================\n")



@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = def_prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)



@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)



@client.event
async def on_command_error(ctx, err):
    try:
        if isinstance(err, errors.CommandNotFound):
            await ctx.message.add_reaction('❌')

        elif isinstance(err, errors.BotMissingPermissions):
            await ctx.send(
                embed=discord.Embed(color=colors['ERROR'],
                                    description=f"The bot has no rights: {' '.join(err.missing_perms)}\nGive them to him for the full functioning of the bot"))
        elif isinstance(err, errors.MissingPermissions) or isinstance(err, errors.CheckFailure):
            await ctx.send(embed=discord.Embed(color=colors['ERROR'],
                                               description=f"You do not have sufficient rights to run this command, or it is disabled!"))
        elif isinstance(err, errors.UserInputError):
            await ctx.send(embed=discord.Embed(color=colors['ERROR'],
                                               description=f"Correct use of the command: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief}): `{ctx.prefix}{ctx.command.usage}`"))

        elif isinstance(err, commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(color=colors['ERROR'],
                                               description=f"You haven't finished your cooldown yet`{ctx.prefix}{ctx.command}`!\nWait: {err.retry_after:.2f} seconds"))
        elif isinstance(err, discord.Forbidden):
            await ctx.send(embed=discord.Embed(color=colors['ERROR'],
                                               description=f"The bot does not have permission to run this command!"))
        else:
            await ctx.send(embed=discord.Embed(color=colors['ERROR'],
                                               description=f"An unknown error occured: \n`{err}`"))
            raise err

    except dpy_errors.Forbidden:
        pass



for file in os.listdir('./Cogs'):
    if file.endswith(".py"):
        client.load_extension(f'Cogs.{file[:-3]}')
        print(f"Загружен ког - {file[:-3]}")


#====================================================

client.run(token)