from discord.ext import commands
import discord, asyncio
from cogs.utils import checks
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

class Admin:
    """Admin only commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def changepresence(self,ctx):
        await self.bot.change_presence(game=discord.Game(name = ctx.message.content.split(' ', 1)[1]))

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def nopresence(self):
        await self.bot.change_presence(game=None)

    def is_pink(self, message):
        return message.author == self.bot.user

    @commands.command(pass_context=True, hidden=True)
    @checks.is_permissive()
    async def pinkdelete(self, ctx):
        message = ctx.message
        if ' ' in message.content:
            print (message.content)
            purge_limit = message.content.split(' ',1)[1]
            if int(purge_limit) > 100:
                await self.bot.say("Can't delete more than 100.")
                return
        else:
            purge_limit = 1
        deleted = await self.bot.purge_from(message.channel, limit=int(purge_limit), check=self.is_pink)
        await self.bot.say('Deleted {} message(s)'.format(len(deleted)))

def setup(bot):
    bot.add_cog(Admin(bot))
