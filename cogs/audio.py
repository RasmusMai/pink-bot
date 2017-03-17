from discord.ext import commands
import discord, asyncio
from cogs.utils import checks
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json
import youtube_dl

class Audio:

    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.player = None

    @commands.command(pass_context=True)
    async def joinvoice(self, ctx):
        if ctx.message.author.voice.voice_channel is not None:
            self.voice = await bot.join_voice_channel()
            await self.bot.say("Joined voice channel "+self.voice.channel.name)
        else:
            await self.bot.say("Please join a voice channel and request again. I can't follow you to nowhere.")

    @commands.command(pass_context=True)
    async def playyoutube(self, ctx, target : str):
        if voice_state_for(self.bot) is None:
            if ctx.message.author.voice.voice_channel is not None:
                self.voice = await bot.join_voice_channel()
                await self.bot.say("Joined voice channel "+self.voice.channel.name)
            else:
                await self.bot.say("Please join a voice channel and request again. I can't follow you to nowhere.")
                return
        target = target.lower()
        if 'youtube.com' not in target:
            await self.bot.say("That's not a youtube link.")
            return
        try:
            self.player = await self.voice.create_ytdl_player(target)
            await self.bot.say("Playing: "+target)
            self.player.start()
        except Exception as e:
            await self.bot.say("Failed to play the requested video, please double check the link.")
            print (e)

    @commands.command()
    async def stopvoice(self, ctx):
        if voice_state_for(self.bot) is None:
            await self.bot.say("I'm not in any voice channels.")
        if self.player.is_playing():
            self.player.stop()
        await self.voice.disconnect()


def setup(bot):
    bot.add_cog(Audio(bot))
