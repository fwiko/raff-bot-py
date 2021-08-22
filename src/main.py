import discord
import json
import datetime

from discord.ext import commands
from collections import namedtuple


class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)


if __name__ == '__main__':

    # config
    config = obj(json.load(open("./config.json", "r")))

    # setting intents to be able to interact with user data
    intents = discord.Intents.default()
    intents.members = True

    # creating the bot obect & setting paramaters
    bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or(config.bot.prefix), owner_id=264375928468013058, intents=intents)
    extensions = config.bot.extensions
    bot.remove_command('help')

    # loading extensions set in the config.json file
    for extension in extensions:
        try:
            bot.load_extension(f"cogs.{extension}.{extension}")
        except Exception as error:
            print(f"{extension} cannot be loaded. [{error}]")
        else:
            print(f"> Loaded {extension}")
    

    @bot.event
    async def on_ready():
        print(f"""
            Logged in...

            Name: {bot.user.name}
            ID: {bot.user.id}
            Author: Rafferty
            Version: 0.0
            Date: {(datetime.datetime.now()).strftime("%d-%m-%Y @ %H:%M:%S")}
        """)
        await bot.change_presence(activity=discord.Game(name=config.bot.status))


    @bot.command()
    @commands.is_owner()
    async def reload(ctx, extension):
        """Reload a module"""
        await ctx.message.delete()
        try:
            if extension in (): # blacklisted reload modules
                await ctx.send(":x: You cannot reload this module.")
            else:
                bot.unload_extension(f"cogs.{extension}.{extension}")
                bot.load_extension(f"cogs.{extension}.{extension}")
                c = discord.Embed(description=f":white_check_mark: Reloaded Extension `{extension}`", colour=config.bot.embed_colour)
                await ctx.send(embed=c)
        except Exception as error:
            c = discord.Embed(description=f"{extension} cannot be reloaded.\n`{error}`", colour=config.bot.embed_colour)
            await ctx.send(embed=c)


    @bot.command()
    @commands.is_owner()
    async def shutdown(ctx):
        await bot.logout()


    bot.run(config.bot.token)