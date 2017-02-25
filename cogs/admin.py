from discord.ext import commands
import discord, asyncio
from cogs.utils import checks
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

class Admin:
    """Admin only commands"""

    def __init__(self, bot):
        self.bot = bot
        if not os.path.isfile('admins.json'):
            with open ('admins.json', 'w') as f:
                f.write('{}')

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def changepresence(self,ctx):
        await self.bot.change_presence(game=discord.Game(name = ctx.message.content.split(' ', 1)[1]))

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def nopresence(self):
        await self.bot.change_presence(game=None)

    @commands.command(pass_context=True, hidden=True)
    @checks.is_admin()
    async def addpermission(self, ctx, target : str):
        server = ctx.message.server
        target_id = target[2:-1]
        with open ('admins.json', 'r') as f:
            admins = json.load(f)
            if str(server.id) not in admins.keys():
                admins[str(server.id)] = []
            if target_id not in admins[str(server.id)]:
                admins[server.id].append(target_id)
                await self.bot.say(target+" has been added to the permissions list.")
            else:
                await self.bot.say(target+" already is in the permissions list.")
        with open ('admins.json', 'w') as f:
            json.dump(admins,f,sort_keys = True,indent = 4)

    @commands.command(pass_context=True,hidden=True)
    @checks.is_admin()
    async def removepermission(self, ctx, target : str):
        server = ctx.message.server
        target_id = target[2:-1]
        with open ('admins.json', 'r') as f:
            admins = json.load(f)
            if str(server.id) not in admins.keys():
                admins[str(server.id)] = []
            if target_id in admins[str(server.id)]:
                admins[server.id].remove(target_id)
                await self.bot.say(target+" has been removed from the permissions list.")
            else:
                await self.bot.say(target+" is not in the permissions list.")
        with open ('admins.json', 'w') as f:
            json.dump(admins,f,sort_keys = True,indent = 4)

    def is_pink(self, message):
        return message.author == self.bot.user

    @commands.command(pass_context=True, hidden=True)
    @checks.is_permissive()
    async def pinkdelete(self, ctx):
        message = ctx.message
        if ' ' in message.content:
            purge_limit = message.content.split(' ',1)[1]
            if int(purge_limit) > 100:
                await self.bot.say("Can't delete more than 100.")
                return
        else:
            await self.bot.say('Please specify the count `pinkdelete <1-100>`. Keep in mind that it also counts messages that aren\'t sent by me')
        deleted = await self.bot.purge_from(message.channel, limit=int(purge_limit), check=self.is_pink)
        await self.bot.say('Deleted {} message(s)'.format(len(deleted)))

def setup(bot):
    bot.add_cog(Admin(bot))
