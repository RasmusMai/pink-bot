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

def setup(bot):
    bot.add_cog(Admin(bot))
