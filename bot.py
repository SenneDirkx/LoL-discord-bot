import os
import discord
import logging
import asyncio
import statistacs
from discord.ext import commands
from commands.voice import Voice

# SETUP!
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)
conn = statistacs.create_connection("./stats.db")
bot = commands.Bot(command_prefix='$')

# Does this function before each command, stores command for stats
@bot.before_invoke
async def common(ctx):
    command = ctx.command.name
    invoker = ctx.author.id
    if len(ctx.args) >= 2:
        target = ctx.args[1]
    else:
        target = None
    invocation = (command, invoker, target)
    #statistacs.add_invocation(conn, invocation)

# When the bot is online, this will be executed
@bot.event
async def on_ready():
    print("And we're ON AIR!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Amy Sonck Insta"))

# When a reaction gets added to a message by the bot, this gets executed
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author.id == 774686931858096149 and user.id != 774686931858096149:
        print("reaction seen")

# report someone, work in progress
@bot.command()
async def reported(ctx, *args):
    if len(args) == 1:
        user_id = args[0].strip("<>@! ")
        user = None
        try:
            user = bot.get_user(int(user_id))
        except:
            user = None
        if user is not None:
            await ctx.send(":boot: Merci voor de report voor <@!{0}>. Ik ga er es na kijke!".format(user.id))
            return
    await ctx.send("Ikke nie denke dat da ene lid van 3600 is. Probeer nog es.")

# Command to organize 5v5, WORK IN PROGRESS
@bot.command(name="5v5")
async def _5v5(ctx, *args):
    if ctx.author.id != 250959871048941568:
        return await ctx.send("Doe maar roestig. Deze functionaliteit is a work in progress.")
    top = discord.utils.get(bot.emojis, name='top')
    jgl = discord.utils.get(bot.emojis, name='jgl')
    mid = discord.utils.get(bot.emojis, name='mid')
    adc = discord.utils.get(bot.emojis, name='adc')
    sup = discord.utils.get(bot.emojis, name='sup')
    embedVar = discord.Embed(title="5v5", description="Used for generating the most equal teams for 5v5 games\n", color=0xa54ad5)
    embedVar.add_field(name="{} TOP".format(top), value="Candidates: ", inline=False)
    embedVar.add_field(name="{} JUNGLE".format(jgl), value="Candidates: ", inline=False)
    embedVar.add_field(name="{} MID".format(mid), value="Candidates: ", inline=False)
    embedVar.add_field(name="{} BOTTOM".format(adc), value="Candidates: ", inline=False)
    embedVar.add_field(name="{} SUPPORT".format(sup), value="Candidates: ", inline=False)
    msg = await ctx.send(embed=embedVar)
    await msg.add_reaction(top)
    await msg.add_reaction(jgl)
    await msg.add_reaction(mid)
    await msg.add_reaction(adc)
    await msg.add_reaction(sup)

# View the stats of all commands ever executed
@bot.command()
async def stats(ctx, *args):
    rows = []
    if len(args) == 0 or (len(args) == 1 and args[0] == "command"):
        rows = statistacs.select_stats_by_field(conn, "command")
    elif len(args) == 1 and args[0] == "subcommand":
        rows = statistacs.select_stats_by_field(conn, "target")
    else:
        return await ctx.send("Die soort **statistacs** ken ik nie, mattie.")
    message = "*STATISTACS*\n"
    for row in rows:
        if row[0] is None:
            continue
        message += " - **" + str(row[0]) + "**: " + str(row[1]) + "\n"
    return await ctx.send(message)

bot.add_cog(Voice(bot))
# Turn on the bot
bot.run(os.getenv("LOLBOT_SECRET_ID"))