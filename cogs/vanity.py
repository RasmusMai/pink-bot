from discord.ext import commands
import discord, asyncio
from .utils import checks
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

class Vanity:
    """Meme commands"""

    def __init__(self, bot):
        self.bot = bot
        self.eightball_array = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it',
        'As I see, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy, try again', 'Ask again later',
        'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'The stars say no',
        'Outlook not so good', 'Very doubtful']

    @commands.command(name="8",aliases=['8ball'])
    async def _8ball(self):
        '''Ask the magic eight ball anything.'''
        await self.bot.say(random.choice(self.eightball_array))

    @commands.command()
    async def source(self):
        '''Returns the link to my source code.'''
        await self.bot.say("My source code is available on github: https://github.com/RasmusMai/pink-bot")

def setup(bot):
    bot.add_cog(Vanity(bot))
