from discord.ext import commands
import discord, asyncio
from .utils import checks
import os, re, time, threading, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

class Vanity:
    """Meme commands"""

    def __init__(self, bot):
        self.bot = bot
        self.eightball_array = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it',
        'As I see, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy, try again', 'Ask again later',
        'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'The stars say no',
        'Outlook not so good', 'Very doubtful']
        self.catfacts_file = 'catfacts.json'
        if not os.path.isfile(self.catfacts_file):
            with open (self.catfacts_file, 'w') as f:
                f.write('{"enabled_servers":[]')

    async def catfacts_loop():
        response = json.loads(urllib.request.urlopen("https://catfacts-api.appspot.com/api/facts").read().decode())
        with open (catfacts_file, 'r') as f:
            catfacts = json.load(f)
            for server in self.bot.servers:
                if server.id in catfacts['enabled_servers']:
                    await self.bot.send_message(server, catfacts['facts'][0])
        threading.Timer(86400, catfacts_loop).start()

    @commands.command(name="8ball")
    async def _8ball(self):
        '''Ask the magic eight ball anything.'''
        await self.bot.say(random.choice(self.eightball_array))

    @commands.command()
    async def source(self):
        '''Returns the link to my source code.'''
        await self.bot.say("My source code is available on github: https://github.com/RasmusMai/pink-bot")

    @commands.command(name="i have no gf", hidden=True)
    async def _ihavenogf(self):
        await self.bot.say("same")

    @commands.command(pass_context=True)
    @checks.is_admin()
    async def togglecatfacts(self):
        with open (self.catfacts_file, 'r') as f:
            catfacts = json.load(f)
            if str(server.id) not in catfacts['enabled_servers']
                catfacts['enabled_servers'].append(str(server.id))
                await self.bot.say("Catfacts have been enabled for this server.")
            else:
                catfacts['enabled_servers'].remove(str(server.id))
                await self.bot.say("Catfacts have been disabled for this server.")
        with open (self.catfacts_file, 'w') as f:
            json.dump(catfacts,f,sort_keys = True,indent = 4)

def setup(bot):
    bot.add_cog(Vanity(bot))
