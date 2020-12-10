from discord.ext import commands
import discord
import asyncio

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Mute everyone in the voice channel you are in
    @commands.command()
    async def m(self, ctx, *args):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.send("Bro, ge zijt nie eens in een voice kanaal?")
        else:
            try:
                voice_client = await ctx.author.voice.channel.connect()
            except:
                voice_client = self.bot.voice_clients[0]
            await self.bot.wait_until_ready()
            memberkeys = ctx.author.voice.channel.voice_states.keys()
            await self.change_mute_state_of_members(ctx, memberkeys, True)

            await self.play_audio_file(voice_client, "mute.mp3", None)

            await voice_client.disconnect()
            message = "Iedereen in `{}` is nu **muted**. *Shhhh, bek toe neven!*".format(ctx.author.voice.channel.name)
            return await ctx.send(message)

    # unmute everyone in the voice channel you are in
    @commands.command()
    async def um(self, ctx, *args):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.send("Bro, ge zijt nie eens in een voice kanaal?")
        else:
            try:
                voice_client = await ctx.author.voice.channel.connect()
            except:
                voice_client = self.bot.voice_clients[0]
            await self.bot.wait_until_ready()
            memberkeys = ctx.author.voice.channel.voice_states.keys()
            await self.change_mute_state_of_members(ctx, memberkeys, False)
            await self.play_audio_file(voice_client, "unmute.mp3", None)
            await voice_client.disconnect()
            message = "Iedereen in `{}` is nu **unmuted**. *Lang leve de vrijheid van meningsuiting!*".format(ctx.author.voice.channel.name)
            return await ctx.channel.send(message)

    async def change_mute_state_of_members(self, ctx, memberkeys, mute):
        for memid in memberkeys:
            member = ctx.guild.get_member(memid)
            if member is not None:
                if member.name == "Rythm" or member.name == "League Of 3600":
                    continue
                await member.edit(mute = mute)
        return True

    # make the bot stop playing sounds
    @commands.command()
    async def shutup(self, ctx, *args):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.send("Bro, ge zijt nie eens in een voice kanaal?")
        try:
            self.bot.voice_clients[0]
        except:
            return await ctx.send("Bro, ben niet eens aant praten?")
        await self.bot.wait_until_ready()
        global allowed_to_play
        allowed_to_play = False
        message = "Allé, ik zal zwijgen :/"
        return await ctx.channel.send(message)

    # Function that plays a certain sound in a voice channel
    async def play_audio_file(self, voice_client, filename, name):
        global allowed_to_play
        await self.bot.wait_until_ready()
        if filename == "./faker.mp3" and name is not None:
            voice_client.play(discord.FFmpegPCMAudio(executable="/Applications/ffmpeg", source="../sounds/"+"fakerP1.mp3"))
            while voice_client.is_playing() and allowed_to_play:
                await asyncio.sleep(0.2)
            voice_client.play(discord.FFmpegPCMAudio(executable="/Applications/ffmpeg", source="../sounds/"+name))
            while voice_client.is_playing() and allowed_to_play:
                await asyncio.sleep(0.2)
            voice_client.play(discord.FFmpegPCMAudio(executable="/Applications/ffmpeg", source="../sounds/"+"fakerP2.mp3"))
            while voice_client.is_playing() and allowed_to_play:
                await asyncio.sleep(0.2)
            return
        voice_client.play(discord.FFmpegPCMAudio(executable="/Applications/ffmpeg", source="../sounds/"+filename))
        await self.bot.wait_until_ready()
        while voice_client.is_playing() and allowed_to_play:
            await asyncio.sleep(0.2)
        if name is not None and allowed_to_play:
            voice_client.play(discord.FFmpegPCMAudio(executable="/Applications/ffmpeg", source="../sounds/"+name))
            await self.bot.wait_until_ready()
            while voice_client.is_playing() and allowed_to_play:
                await asyncio.sleep(0.2)
        allowed_to_play = True
    
    # make the bot say something in voice
    @commands.command()
    async def say(self, ctx, *args):
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
            voice_client = self.bot.voice_clients[0]
        
        await self.play_audio_file(voice_client, filename, name)
        await voice_client.disconnect()