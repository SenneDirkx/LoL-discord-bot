import os
import discord
import logging
import asyncio
import statistacs
from discord.ext import commands

# SETUP!
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)
conn = statistacs.create_connection("./stats.db")
bot = commands.Bot(command_prefix='$')

allowed_to_play = True

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
    statistacs.add_invocation(conn, invocation)

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

# make the bot say something in voice
@bot.command()
async def say(ctx, *args):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        return await ctx.send("Bro, ge zijt nie eens in een voice kanaal?")
    options = {
        "stfu": "mute.mp3",
        "speakup": "unmute.mp3",
        "wamake": "audio.m4a",
        "ggez": "ggez.mp3",
        "kk": "kk.mp3",
        "0/10": "powerspiku.mp3",
        "penta": "penta2.mp3",
        "faker": "faker.mp3",
        "xpeke": "xpeke.mp3",
        "disrespect": "disrespect.mp3",
        "ahhh": "ahhh.mp3",
        "hooo": "hooo.mp3"
    }
    if len(args) == 0:
        message = "Dit zijn de available sounds: \n"
        for key in options.keys():
            message += "**" + key + "**\n"
        return await ctx.send(message)
    filename = options.get(args[0],None)
    if filename is None:
        return await ctx.send("Da is nie eens een viable sound, my G?")
    name = None
    if len(args) == 2:
        name_options = {
            "anthony": "anthony.mp3",
            "hans": "hans.mp3",
            "jasper": "jasper.m4a",
            "luca": "luca.mp3",
            "matthias": "matthias.mp3",
            "maxim": "maxim.mp3",
            "pieter": "pieter.mp3",
            "senne": "senne.mp3",
            "wout": "wout.mp3",
            "xander": "xander.mp3"
        }
        name = name_options.get(args[1],None)
        if name is None:
            return await ctx.send("Die neef ken ik niet. *$say <sound> [<name>]*")
    try:
        voice_client = await ctx.author.voice.channel.connect()
    except:
        voice_client = bot.voice_clients[0]
    
    await play_audio_file(voice_client, filename, name)
    await voice_client.disconnect()

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

# Mute everyone in the voice channel you are in
@bot.command()
async def m(ctx, *args):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        return await ctx.send("Bro, ge zijt nie eens in een voice kanaal?")
    else:
        try:
            voice_client = await ctx.author.voice.channel.connect()
        except:
            voice_client = bot.voice_clients[0]
        await bot.wait_until_ready()
        memberkeys = ctx.author.voice.channel.voice_states.keys()
        await change_mute_state_of_members(ctx, memberkeys, True)

        await play_audio_file(voice_client, "./mute.mp3")

        await voice_client.disconnect()
        message = "Iedereen in `{}` is nu **muted**. *Shhhh, bek toe neven!*".format(ctx.author.voice.channel.name)
        return await ctx.send(message)

# unmute everyone in the voice channel you are in
@bot.command()
async def um(ctx, *args):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        return await ctx.send("Bro, ge zijt nie eens in een voice kanaal?")
    else:
        try:
            voice_client = await ctx.author.voice.channel.connect()
        except:
            voice_client = bot.voice_clients[0]
        await bot.wait_until_ready()
        memberkeys = ctx.author.voice.channel.voice_states.keys()
        await change_mute_state_of_members(ctx, memberkeys, False)
        await play_audio_file(voice_client, "./unmute.mp3")
        await voice_client.disconnect()
        message = "Iedereen in `{}` is nu **unmuted**. *Lang leve de vrijheid van meningsuiting!*".format(ctx.author.voice.channel.name)
        return await ctx.channel.send(message)

async def change_mute_state_of_members(ctx, memberkeys, mute):
    for memid in memberkeys:
        member = ctx.guild.get_member(memid)
        if member is not None:
            if member.name == "Rythm" or member.name == "League Of 3600":
                continue
            await member.edit(mute = mute)
    return True

# make the bot stop playing sounds
@bot.command()
async def shutup(ctx, *args):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        return await ctx.send("Bro, ge zijt nie eens in een voice kanaal?")
    try:
        bot.voice_clients[0]
    except:
        return await ctx.send("Bro, ben niet eens aant praten?")
    await bot.wait_until_ready()
    global allowed_to_play
    allowed_to_play = False
    message = "Allé, ik zal zwijgen :/"
    return await ctx.channel.send(message)

# Function that plays a certain sound in a voice channel
async def play_audio_file(voice_client, filename, name):
    global allowed_to_play
    await bot.wait_until_ready()
    if filename == "./faker.mp3" and name is not None:
        voice_client.play(discord.FFmpegPCMAudio(executable="/Applications/ffmpeg", source="./sounds/"+"fakerP1.mp3"))
        while voice_client.is_playing() and allowed_to_play:
            await asyncio.sleep(0.2)
        voice_client.play(discord.FFmpegPCMAudio(executable="/Applications/ffmpeg", source="./sounds/"+name))
        while voice_client.is_playing() and allowed_to_play:
            await asyncio.sleep(0.2)
        voice_client.play(discord.FFmpegPCMAudio(executable="/Applications/ffmpeg", source="./sounds/"+"fakerP2.mp3"))
        while voice_client.is_playing() and allowed_to_play:
            await asyncio.sleep(0.2)
        return
    voice_client.play(discord.FFmpegPCMAudio(executable="/Applications/ffmpeg", source="./sounds/"+filename))
    await bot.wait_until_ready()
    while voice_client.is_playing() and allowed_to_play:
        await asyncio.sleep(0.2)
    if name is not None and allowed_to_play:
        voice_client.play(discord.FFmpegPCMAudio(executable="/Applications/ffmpeg", source="./sounds/"+name))
        await bot.wait_until_ready()
        while voice_client.is_playing() and allowed_to_play:
            await asyncio.sleep(0.2)
    allowed_to_play = True

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

# Turn on the bot
bot.run(os.getenv("LOLBOT_SECRET_ID"))