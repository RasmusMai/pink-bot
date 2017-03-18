from discord.ext import commands
import discord, asyncio
from .utils import checks
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

class Stats:
    '''Statistics'''

    def __init__(bot, self):
        self.bot = bot

    @commands.command(pass_conext=True, no_pm=True)
    async def serverinfo(self, ctx):
        '''Displays info about the serverinfo

        Includes information like the user count, date of birth and a lot more.'''
        server = ctx.message.server
        online_count = len([m.status for m in server.members if m.status == discord.Status.online or m.status == discord.Status.idle])
        user_count = len(server.members)
        text_channels = len([x for x in server.channels if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        days_passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Anno "+server.created_at.strftime("%d %b %Y %H:%M")+". "+days_passed+" days ago.")
        color = discord.Color(random.randint(0,16777215))
        embed = discord.Embed(description=created_at, colour=color)
        embed.add_field(name="Region", value=str(server.region))
        embed.add_field(name="Users", value=online_count+"/"+user_count)
        embed.add_field(name="Text Channels", value=text_channels)
        embed.add_field(name="Voice Channels", value=voice_channels)
        embed.add_field(name="Roles", value=len(server.roles))
        embed.add_field(name="Owner", value=str(server.owner))
        if server.icon_url:
            embed.set_author(name=server.name, url=server.icon_url)
            embed.set_thumbnail(url=server.icon_url)
        else:
            embed.set_author(name=server.name)
        await self.bot.say(embed=data)

def setup(bot):
    bot.add_cog(Stats(bot))
